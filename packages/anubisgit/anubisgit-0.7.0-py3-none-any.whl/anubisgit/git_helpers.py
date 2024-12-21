"""All the git helpers for anubisgit"""

from os import stat
from os.path import splitext, isfile
import re
import subprocess
from typing import Tuple, Union, List
from loguru import logger
from datetime import datetime
from fileinput import filename


def parse_git_show_stats(show_lines: str, rev: str, br_type: str) -> dict:
    """
    Parser for git stats, this will return a dict containing the author name with his insertions
    and deletions.

    Args:
        show_lines (str): Lines of code
        rev (str): Name of the current git revision
        br_type (str): Name of the branch currently analyzed

    Returns:
        out (dict): Dictionnary of the git stats
    """
    out = {
        "author": None,
        "date": None,
        "files": 0,
        "insertions": 0,
        "deletions": 0,
        "revision": rev,
        "br_type": br_type,
        # "raw": show_lines ## For debug, but very heavy
    }
    for line in show_lines.split("\n"):
        if line.startswith("Author:"):
            out["author"] = line[7:].split("<")[0].strip()
        if line.startswith("Date:"):
            out["date"] = line[5:].strip()

        ref = [" changed", " insertion", " deletion"]
        val = sum(
            [i in line for i in ref]
        )  # here we sum booleans in order to check that at least 2 keywords of ref are present in line
        if val >= 2:
            (out["files"], out["insertions"], out["deletions"]) = _read_diff(line)
    return out


def _read_diff(diffstr: str) -> Tuple[int, int, int]:
    """
    Compute the difference of lines in between git commits i.e.
    the changes that occured in a file.

    Args:
        diffstr (str): String where the difference between lines have been referenced.

    Returns:
        files (int): Number of filed changed
        insertions (int): Number of insertions made to the code
        deletions (int): Number of deletions made to the code
    """
    files = 0
    insertions = 0
    deletions = 0
    for mention in diffstr.split(","):
        if "changed" in mention:
            found = [int(s) for s in mention.strip().split() if s.isdigit()]
            files = found[0]
        if "insertion" in mention:
            found = [int(s) for s in mention.strip().split() if s.isdigit()]
            insertions = found[0]
        if "deletion" in mention:
            found = [int(s) for s in mention.strip().split() if s.isdigit()]
            deletions = found[0]

    return files, insertions, deletions


def git_last_revision(date: datetime, branch: str) -> Union[None, str]:
    """
    Get the last revision before a date

    Args:
        date (datetime.time) : Date from which the last revision will be searched
        branch (str): Name of the branch on which to search

    Returns:
        Union[None,str]: Nothing if revision could not be found. Name of the revision
        as a string otherwise.
    """

    logger.info(f"... searching for last revision before {date}")

    sp = subprocess.run(
        ["git", "rev-list", "-n 1", "--first-parent", f"--before={date}", branch],
        capture_output=True,
    )
    if sp.returncode == 0:
        revision = sp.stdout.decode()
        if revision == "":
            logger.warning("... No revision before this date")
            return None
        else:
            logger.success("Revision found, continuing ...")
            return revision.rstrip("\n")

    else:
        logger.warning("... Git get revision failed")
        return None


def git_revision_in_between(
    after_date: datetime, before_date: datetime, branch: str = "--all"
) -> Union[list, None]:
    """
    Get the last revision between dates

    Args:
        after_date (datetime): Date to start from
        before_date (datetime): Date to end before
        branch (str, optional): Name of the branch. Defaults to "--all".

    Returns:
        Union[list,None]: Either a list with the revisions or None.
    """
    sp = subprocess.run(
        [
            "git",
            "rev-list",
            f"--before={before_date}",
            f"--after={after_date}",
            branch,
        ],
        capture_output=True,
    )
    if sp.returncode != 0:
        logger.warning("Git get revision failed")
        return None
    out = sp.stdout.decode()
    if out == "":
        logger.warning("... No revisions found")
        return []
    revision_list = out.strip().split("\n")
    return revision_list


def git_revision_stats(
    branch: str,
    revision_list_main: list,
    revision_list_all: list,
    other_filter: bool = True,
    common_commit: dict = None,
) -> Union[None, list]:
    """Get the stats revision in between dates

    Args:
        branch (str): Name of the branch
        revision_list_main (list): List of revision of the branch
        revision_list_all (list): List of revision of all branches
        other_filter (bool): True if apply "other" filter in branches. Defaults to True.
        common_commit (dict): Only use when other_filter is False. Each branch's commit hash of the most recent common ancestor with dev branch. Defaults to None.

    Returns:
        Union[None,List]: None if unable ot find a revision, list of commits stats otherwise.

    """

    logger.info("... gathering commits stats")

    stats_commits = []
    for rev in revision_list_all:
        sp = subprocess.run(
            [
                "git",
                "show",
                rev,
                "--shortstat",
            ],
            capture_output=True,
        )

        if sp.returncode != 0:
            pass
        else:
            if other_filter:
                br_type = "other"

                if rev in revision_list_main:
                    br_type = branch
            else:
                br_type = git_select_branches(rev, common_commit, branch)

            try:
                show_lines = sp.stdout.decode("utf-8")
            except UnicodeDecodeError:
                show_lines = sp.stdout.decode("latin-1")

            stats_commits.append(parse_git_show_stats(show_lines, rev, br_type))
    logger.success("Commits stats obtained, continuing ...")
    return stats_commits


def git_checkout(revision: str) -> None:
    """
    Git checkout by revision

    Args:
        revision (str): Name of the revision
    """
    logger.debug(f"... checkout revision {revision}")

    # Leave -fd in the git checkout to avoid crash from forced commit in older revision
    sp = subprocess.run(["git", "checkout", "-f", revision], capture_output=True)
    if sp.returncode == 0:
        logger.success("Checkout completed, continuing ...")
        return None
    else:
        logger.warning(f"Could not checkout on revision {revision}\n" + str(sp))


def git_blame(path: str, print_log=True) -> dict:
    """
    Git blame for each code file in given directory

    Git blame is applied to code files only, determined by their extension or their name.

    For each file, `git_blame` retrieves for each non blank code line the following information:
        - last author
        - last modification date
        - number of indentation (i.e. number of blank before first non blank character)

    Args:
        path (str): Relative path to sources

    Returns:
        blame_info (dict): Contains git blame information for each code file in source directory
    """
    if print_log:
        logger.info(f"... get git blame info")

    blame_info = []
    # get list of files in source directory
    list_files = git_ls_files(path)
    for file_ in list_files:
        # check if the file in cloc list
        filename = file_.decode("utf-8")
        # use blame only on source file
        _, file_extension = splitext(filename)
        blame_dict = {}
        if file_extension.replace(".", "") in CLOC_LANGUAGE_BY_EXTENSIONS.keys():
            # get blame info for the file
            blame_dict["file"] = filename
            blame_dict.update(_blame_file(file_))
            blame_info.append(blame_dict)
    logger.success("Git blame infos obtained, continuing ...")
    return blame_info


def git_ls_files(path: list) -> list:
    """
    Execute the command git ls-files for a list of paths, then gather the result in a list.

    Args:
        path (list): List of path for which you want to run the command

    Returns:
        list: Concatenated output from the git ls-files executed.
    """
    list_files = []
    for path_ in path:
        sp = subprocess.run(["git", "ls-files", "--", path_], capture_output=True)
        if sp.stdout.strip():
            # parse files to blame
            list_files += sp.stdout.splitlines()

    return list_files


def _blame_file(filepath: str) -> Union[None, dict]:
    """
    Get git blame information about a file

    Args:
        filepath (str): File path

    Returns:
        Union [None,dict]: None if unable to find date on blamed file.
        Contains for each non blank code line (author name, last modification, indentation)
    """
    date_regex = r"(\d\d\d\d-\d\d-\d\d)"
    data = {
        "author": [],
        "date": [],
        "indentation": [],
        "line_number": [],
    }
    # run git blame
    sp = subprocess.run(
        ["git", "blame", "-c", filepath],
        capture_output=True,
    )
    if sp.returncode == 0:
        # parse files to blame
        for lineraw in sp.stdout.splitlines():
            # decode line
            line = lineraw.decode("utf-8", errors="ignore")
            # get the code
            codeline = ")".join(line.split(")")[1:])
            length_no_space = len(codeline.lstrip())
            if length_no_space == 0:
                # if line is blank go to next line
                continue

            try:
                date = re.findall(date_regex, line)[0]
            except IndexError:
                logger.warning(
                    f"Could not blame file: {filename}, dates not available\n"
                )
                return data
            # store infos

            enclosed = ""
            level = 0
            pos = 0
            for char in line:
                pos += 1
                if char == "(":
                    level += 1
                if char == ")":
                    level -= 1
                if level == 1:
                    if char not in "()":
                        enclosed += char
                if level == 0 and enclosed != "":
                    break

            codeline = line[pos:]
            indent_spaces = len(codeline) - len(codeline.lstrip()) - 1
            items = enclosed.split()
            line = int(items[-1])

            author = " ".join(items[:-4])

            data["author"].append(author)
            data["date"].append(date)
            data["indentation"].append(indent_spaces)
            data["line_number"].append(line)
        return data
    else:
        logger.warning(f"Could not blame file: {filename}\n" + str(sp))
        return None


def git_branch_status(ref_commit: str, date: str, ref_branch: str) -> Union[None, list]:
    """
    Get branch status for each branch

    Args:
        ref_commit  (str): Reference commit (on reference branch)
        date        (str): Reference date for the branch status
        ref_branch  (str): Reference branch

    Returns:
        Union [None,list]: None if unable to git branch the specified branch.
        Contains branch status for each branch otherwise.
    """
    logger.info(f"... branch status")
    # get all branches
    sp = subprocess.run(["git", "branch", "-a"], capture_output=True)
    if sp.returncode == 0:
        # parse branches
        list_branch = [
            s.lstrip() for s in sp.stdout.decode("utf-8", errors="ignore").splitlines()
        ]

        # remove reference branch in the list
        try:
            list_branch.remove(ref_branch)
        except ValueError:
            logger.warning(f"<{ref_branch}> was not found in git branch -a")

        # count nb of commit on ref branch
        sp = subprocess.run(
            ["git", "rev-list", "--count", ref_commit],
            capture_output=True,
        )
        if sp.returncode == 0:
            nb_commits_ref_branch = int(sp.stdout.decode())

        # init list of branch data
        branch_data = []
        for branch in list_branch:
            # retrieve last commit before `date` for current branch
            sp = subprocess.run(
                [
                    "git",
                    "rev-list",
                    "--first-parent",
                    "-n 1",
                    f"--before={date}",
                    branch,
                ],
                capture_output=True,
            )
            if sp.returncode == 0:
                revision = sp.stdout.decode()
                if revision == "":
                    continue
                else:
                    branch_commit = revision.rstrip("\n")
            else:
                if "HEAD" not in branch:
                    logger.warning(f".... Git get revision for branch {branch} failed")
                continue

            # check if reference commit is the same than branch commit (ie branch does not exist at this time)
            if ref_commit in [branch_commit]:
                continue

            # get branch status
            sp = subprocess.run(
                [
                    "git",
                    "rev-list",
                    "--left-right",
                    "--count",
                    f"{ref_commit}...{branch_commit}",
                ],
                capture_output=True,
            )
            if sp.returncode == 0:
                # parse output
                raw_data = (
                    sp.stdout.decode("utf-8", errors="ignore").rstrip().split("\t")
                )
                # add data to list
                branch_data.append(
                    {
                        "branch": branch,
                        "behind": int(raw_data[0]),
                        "ahead": int(raw_data[1]),
                        "nb_commits_ref_branch": nb_commits_ref_branch,
                    }
                )
            else:
                logger.warning(f"branch {branch} was not processed")
        logger.success("Branches status obtained, continuing ...")
        return branch_data
    else:
        logger.warning(f"Could not get git branch" + str(sp))
        return None


def git_branch_list() -> list:
    """Find all the branches in the repo.

    Returns:
        list: Names of branches
    """
    logger.info(f"... branch status")
    # get all branches
    sp = subprocess.run(["git", "branch", "-a"], capture_output=True)
    if sp.returncode == 0:
        # parse branches
        list_branch = [
            s.lstrip() for s in sp.stdout.decode("utf-8", errors="ignore").splitlines()
        ]
        # Delete HEAD branch
        clean_list_branch = [
            name.strip("* ") for name in list_branch if "HEAD" not in name
        ]
        return clean_list_branch
    else:
        logger.warning(f"Could not get git branch" + str(sp))
        return None


def git_merge_branch(ref_branch: str) -> dict:
    """Find the most recent common ancestor with dev branch of all branches in the repo.

    Args:
        ref_branch (str): Dev branch name.

    Returns:
        dict: Each branch's commit hash of the most recent common ancestor with dev branch.
    """

    list_branch = git_branch_list()

    common_commit = {}
    for branch in list_branch:
        sp = subprocess.run(
            ["git", "merge-base", branch, ref_branch], capture_output=True
        )
        if sp.returncode == 0:
            common_commit[branch] = sp.stdout.decode().strip()
        else:
            logger.warning(
                f"Could not get common ancestor with {ref_branch} and {branch}"
            )
            common_commit[branch] = None
    return common_commit


def git_select_branches(rev: str, refs_commit: dict, dev_branch: str) -> list:
    """Finds all branches containing a revision.

    Note:
        Because of the way Git works, branches have in their history all commits made before they were created.
        To improve the result of "git branch --contains", this function applies a filter using the most recent
        common ancestor with dev branch. Thus, rev is considered to be contained by a branch if it's older than
        the split between the branch and the dev branch - so it doesn't means that it's exactly ON the branch.
        (this is only the case if the dev branch is its parent branch)

    Args:
        rev (str): Name of the current revision.
        refs_commit (dict): Dict of most recent common ancestor with dev branch for all branches.
        dev_branch (str): Dev branch name.

    Returns:
        list: List of branches that have rev in their history.
    """

    on_branch = []

    # Finds all the branches that have rev in their history.
    branch_sp = subprocess.run(
        ["git", "branch", "-a", "--contains", rev],
        capture_output=True,
    )

    if branch_sp.returncode == 0:
        clean_list_branch = [
            s.lstrip()
            for s in branch_sp.stdout.decode("utf-8", errors="ignore").splitlines()
            if "HEAD" not in s
        ]
        # Filter branches based on their most recent common ancestor with dev branch.
        # If rev is after the most recent common ancestor, it is likely that rev belongs to the branch.
        for br in clean_list_branch:
            if br != dev_branch and refs_commit[br] is not None:
                # Gives which commit is first.
                sp = subprocess.run(
                    ["git", "merge-base", rev, refs_commit[br]], capture_output=True
                )
                if sp.returncode == 0:
                    first_commit = sp.stdout.decode().strip()
                    if first_commit == refs_commit[br] and rev != first_commit:
                        on_branch.append(br)
                else:
                    logger.warning(
                        f"No relation with {rev} and {refs_commit[br]} found."
                    )
            else:
                on_branch.append(br)
    else:
        logger.warning(f"No references for {rev} found.")
    return on_branch


def git_size(path: str, previous_size: float = 0.0) -> Union[dict, float]:
    """
    Get git repository size in bytes

    This funtion relies on `os.stat.st_size` which gives the "size in bytes of a plain file; amount of data waiting on some special files".

    See official documentation of `os.stats.st_size` for more information about the size computation.

    Args:
        path (str): Relative path to sources

    Returns:
        Union[dict,float]: Empty dict if error in fit size, otherwise size of the repository (bytes)
    """
    logger.info(f"... git repository size")
    list_files = git_ls_files(path)
    # get size in bytes for each file
    gitsize = previous_size
    for file_ in list_files:
        if isfile(file_):
            gitsize += stat(file_).st_size

    logger.success("Git repository size obtained, continuing ...")
    return gitsize


def git_tag_history(ref_branch: str) -> dict:
    """
    Get tag dates for a given branch

    Args:
        ref_branch  (str): Reference branch

    Returns:
        tags_date (dict): dict of tag name and date
    """
    logger.info(f"... tag history on branch: {ref_branch}")
    # get list of commits on the ref branch
    sp = subprocess.run(
        [
            "git",
            "rev-list",
            "--first-parent",
            ref_branch,
        ],
        capture_output=True,
    )
    if sp.returncode == 0:
        list_commits = sp.stdout.decode().splitlines()
    else:
        logger.error(f"error in git_tag_history: {sp.stderr}")
        return {}

    # get list of tags
    sp = subprocess.run(
        [
            "git",
            "tag",
        ],
        capture_output=True,
    )
    if sp.returncode == 0:
        list_tag = sp.stdout.decode().splitlines()
    else:
        logger.error(f"error in git_tag_history: {sp.stderr}")
        return {}

    tags_date = {}
    # for each tag get commit hash and date
    for tag in list_tag:
        sp = subprocess.run(
            [
                "git",
                "show",
                "-s",
                "--no-notes",
                "--format=%H %aI",
                f"{tag}^",
            ],
            capture_output=True,
        )
        if sp.returncode == 0:
            [tag_commit, tag_date] = sp.stdout.decode().splitlines()[-1].split()
            if tag_commit in list_commits:
                tags_date[tag] = tag_date

    return tags_date


# TODO : Put that in antoher file to import from.

CLOC_LANGUAGE_BY_EXTENSIONS = {
    "abap": "ABAP",
    "ac": "m4",
    "ada": "Ada",
    "adb": "Ada",
    "ads": "Ada",
    "adso": "ADSO/IDSM",
    "ahkl": "AutoHotkey",
    "ahk": "AutoHotkey",
    "agda": "Agda",
    "lagda": "Agda",
    "aj": "AspectJ",
    "am": "make",
    "ample": "AMPLE",
    "apl": "APL",
    "apla": "APL",
    "aplf": "APL",
    "aplo": "APL",
    "apln": "APL",
    "aplc": "APL",
    "apli": "APL",
    "dyalog": "APL",
    "dyapp": "APL",
    "mipage": "APL",
    "as": "ActionScript",
    "adoc": "AsciiDoc",
    "asciidoc": "AsciiDoc",
    "dofile": "AMPLE",
    "startup": "AMPLE",
    "axd": "ASP",
    "ashx": "ASP",
    "asa": "ASP",
    "asax": "ASP.NET",
    "ascx": "ASP.NET",
    "asd": "Lisp",  # system definition file
    "nasm": "Assembly",
    "a51": "Assembly",
    "asm": "Assembly",
    "asmx": "ASP.NET",
    "asp": "ASP",
    "aspx": "ASP.NET",
    "master": "ASP.NET",
    "sitemap": "ASP.NET",
    "cshtml": "Razor",
    "razor": "Razor",  # Client-side Blazor
    "nawk": "awk",
    "mawk": "awk",
    "gawk": "awk",
    "auk": "awk",
    "awk": "awk",
    "bash": "Bourne Again Shell",
    "bazel": "Starlark",
    "BUILD": "Bazel",
    "dxl": "DOORS Extension Language",
    "bat": "DOS Batch",
    "BAT": "DOS Batch",
    "cmd": "DOS Batch",
    "CMD": "DOS Batch",
    "btm": "DOS Batch",
    "BTM": "DOS Batch",
    "blade": "Blade",
    "blade.php": "Blade",
    "build.xml": "Ant",
    "b": "Brainfuck",
    "bf": "Brainfuck",
    "brs": "BrightScript",
    "bzl": "Starlark",
    "btp": "BizTalk Pipeline",
    "odx": "BizTalk Orchestration",
    "cpy": "COBOL",
    "cobol": "COBOL",
    "ccp": "COBOL",
    "cbl": "COBOL",
    "CBL": "COBOL",
    "idc": "C",
    "cats": "C",
    "c": "C",
    "tpp": "C++",
    "tcc": "C++",
    "ipp": "C++",
    "inl": "C++",
    "h++": "C++",
    "C": "C++",
    "cc": "C++",
    "c++": "C++",
    "ccs": "CCS",
    "cfc": "ColdFusion CFScript",
    "cfml": "ColdFusion",
    "cfm": "ColdFusion",
    "chpl": "Chapel",
    "cl": "Lisp/OpenCL",
    "riemann.config": "Clojure",
    "hic": "Clojure",
    "cljx": "Clojure",
    "cljscm": "Clojure",
    "cljs.hl": "Clojure",
    "cl2": "Clojure",
    "boot": "Clojure",
    "clj": "Clojure",
    "cljs": "ClojureScript",
    "cljc": "ClojureC",
    "cls": "Visual Basic/TeX/Apex Class",
    "cmake.in": "CMake",
    "CMakeLists.txt": "CMake",
    "cmake": "CMake",
    "cob": "COBOL",
    "COB": "COBOL",
    "iced": "CoffeeScript",
    "cjsx": "CoffeeScript",
    "cakefile": "CoffeeScript",
    "_coffee": "CoffeeScript",
    "coffee": "CoffeeScript",
    "component": "Visualforce Component",
    "cpp": "C++",
    "CPP": "C++",
    "cr": "Crystal",
    "cs": "C#/Smalltalk",
    "designer.cs": "C# Designer",
    "cake": "Cake Build Script",
    "csh": "C Shell",
    "cson": "CSON",
    "css": "CSS",
    "csv": "CSV",
    "cu": "CUDA",
    "cuh": "CUDA",  # CUDA header file
    "cxx": "C++",
    "d": "D/dtrace",
    # in addition, .d can map to init.d files typically written as
    # bash or sh scripts
    "da": "DAL",
    "dart": "Dart",
    "dsc": "DenizenScript",
    "derw": "Derw",
    "def": "Windows Module Definition",
    "dhall": "dhall",
    "dt": "DIET",
    "patch": "diff",
    "diff": "diff",
    "dmap": "NASTRAN DMAP",
    "sthlp": "Stata",
    "matah": "Stata",
    "mata": "Stata",
    "ihlp": "Stata",
    "doh": "Stata",
    "ado": "Stata",
    "do": "Stata",
    "DO": "Stata",
    "Dockerfile": "Dockerfile",
    "dockerfile": "Dockerfile",
    "pascal": "Pascal",
    "lpr": "Pascal",
    "dfm": "Delphi Form",
    "dpr": "Pascal",
    "dita": "DITA",
    "drl": "Drools",
    "dtd": "DTD",
    "ec": "C",
    "ecpp": "ECPP",
    "eex": "EEx",
    "el": "Lisp",
    "elm": "Elm",
    "exs": "Elixir",
    "ex": "Elixir",
    "ecr": "Embedded Crystal",
    "ejs": "EJS",
    "erb": "ERB",
    "ERB": "ERB",
    "yrl": "Erlang",
    "xrl": "Erlang",
    "rebar.lock": "Erlang",
    "rebar.config.lock": "Erlang",
    "rebar.config": "Erlang",
    "emakefile": "Erlang",
    "app.src": "Erlang",
    "erl": "Erlang",
    "exp": "Expect",
    "4th": "Forth",
    "fish": "Fish Shell",
    "fnl": "Fennel",
    "forth": "Forth",
    "fr": "Forth",
    "frt": "Forth",
    "fth": "Forth",
    "f83": "Forth",
    "fb": "Forth",
    "fpm": "Forth",
    "e4": "Forth",
    "rx": "Forth",
    "ft": "Forth",
    "f77": "Fortran 77",
    "F77": "Fortran 77",
    "f90": "Fortran 90",
    "F90": "Fortran 90",
    "f95": "Fortran 95",
    "F95": "Fortran 95",
    "f": "Fortran 77/Forth",
    "F": "Fortran 77",
    "for": "Fortran 77/Forth",
    "FOR": "Fortran 77",
    "ftl": "Freemarker Template",
    "ftn": "Fortran 77",
    "FTN": "Fortran 77",
    "fmt": "Oracle Forms",
    "focexec": "Focus",
    "fs": "F#/Forth",
    "fsi": "F#",
    "fsx": "F# Script",
    "fxml": "FXML",
    "gnumakefile": "make",
    "Gnumakefile": "make",
    "gd": "GDScript",
    "gdshader": "Godot Shaders",
    "vshader": "GLSL",
    "vsh": "GLSL",
    "vrx": "GLSL",
    "gshader": "GLSL",
    "glslv": "GLSL",
    "geo": "GLSL",
    "fshader": "GLSL",
    "fsh": "GLSL",
    "frg": "GLSL",
    "fp": "GLSL",
    "fbs": "Flatbuffers",
    "glsl": "GLSL",
    "graphqls": "GraphQL",
    "gql": "GraphQL",
    "graphql": "GraphQL",
    "vert": "GLSL",
    "tesc": "GLSL",
    "tese": "GLSL",
    "geom": "GLSL",
    "feature": "Cucumber",
    "frag": "GLSL",
    "comp": "GLSL",
    "g": "ANTLR Grammar",
    "g4": "ANTLR Grammar",
    "gleam": "Gleam",
    "go": "Go",
    "gsp": "Grails",
    "jenkinsfile": "Groovy",
    "gvy": "Groovy",
    "gtpl": "Groovy",
    "grt": "Groovy",
    "groovy": "Groovy",
    "gant": "Groovy",
    "gradle": "Gradle",
    "gradle.kts": "Gradle",
    "h": "C/C++ Header",
    "H": "C/C++ Header",
    "hh": "C/C++ Header",
    "hpp": "C/C++ Header",
    "hxx": "C/C++ Header",
    "hb": "Harbour",
    "hrl": "Erlang",
    "hsc": "Haskell",
    "hs": "Haskell",
    "tfvars": "HCL",
    "hcl": "HCL",
    "tf": "HCL",
    "nomad": "HCL",
    "hlsli": "HLSL",
    "fxh": "HLSL",
    "hlsl": "HLSL",
    "shader": "HLSL",
    "cg": "HLSL",
    "cginc": "HLSL",
    "haml.deface": "Haml",
    "haml": "Haml",
    "handlebars": "Handlebars",
    "hbs": "Handlebars",
    "hxsl": "Haxe",
    "hx": "Haxe",
    "hoon": "Hoon",
    "xht": "HTML",
    "html.hl": "HTML",
    "htm": "HTML",
    "html": "HTML",
    "heex": "HTML EEx",
    "i3": "Modula3",
    "ice": "Slice",
    "icl": "Clean",
    "dcl": "Clean",
    "dlm": "IDL",
    "idl": "IDL",
    "idr": "Idris",
    "lidr": "Literate Idris",
    "imba": "Imba",
    "prefs": "INI",
    "lektorproject": "INI",
    "buildozer.spec": "INI",
    "ini": "INI",
    "ism": "InstallShield",
    "ipl": "IPL",
    "pro": "IDL/Qt Project/Prolog/ProGuard",
    "ig": "Modula3",
    "il": "SKILL",
    "ils": "SKILL++",
    "inc": "PHP/Pascal",  # might be PHP or Pascal
    "inl": "C++",
    "ino": "Arduino Sketch",
    "ipf": "Igor Pro",
    "pde": "Arduino Sketch",  # pre 1.0
    "itk": "Tcl/Tk",
    "java": "Java",
    "jcl": "JCL",  # IBM Job Control Lang.
    "jl": "Lisp/Julia",
    "xsjslib": "JavaScript",
    "xsjs": "JavaScript",
    "ssjs": "JavaScript",
    "sjs": "JavaScript",
    "pac": "JavaScript",
    "njs": "JavaScript",
    "mjs": "JavaScript",
    "cjs": "JavaScript",
    "jss": "JavaScript",
    "jsm": "JavaScript",
    "jsfl": "JavaScript",
    "jscad": "JavaScript",
    "jsb": "JavaScript",
    "jakefile": "JavaScript",
    "jake": "JavaScript",
    "bones": "JavaScript",
    "_js": "JavaScript",
    "js": "JavaScript",
    "es6": "JavaScript",
    "jsf": "JavaServer Faces",
    "jsx": "JSX",
    "xhtml": "XHTML",
    "jinja": "Jinja Template",
    "jinja2": "Jinja Template",
    "yyp": "JSON",
    "webmanifest": "JSON",
    "webapp": "JSON",
    "topojson": "JSON",
    "tfstate.backup": "JSON",
    "tfstate": "JSON",
    "mcmod.info": "JSON",
    "mcmeta": "JSON",
    "json-tmlanguage": "JSON",
    "jsonl": "JSON",
    "har": "JSON",
    "gltf": "JSON",
    "geojson": "JSON",
    "composer.lock": "JSON",
    "avsc": "JSON",
    "watchmanconfig": "JSON",
    "tern-project": "JSON",
    "tern-config": "JSON",
    "htmlhintrc": "JSON",
    "arcconfig": "JSON",
    "json": "JSON",
    "json5": "JSON5",
    "jsp": "JSP",  # Java server pages
    "jspf": "JSP",  # Java server pages
    "junos": "Juniper Junos",
    "vm": "Velocity Template Language",
    "ksc": "Kermit",
    "ksh": "Korn Shell",
    "ktm": "Kotlin",
    "kt": "Kotlin",
    "kts": "Kotlin",
    "hlean": "Lean",
    "lean": "Lean",
    "lhs": "Haskell",
    "lex": "lex",
    "l": "lex",
    "lem": "Lem",
    "less": "LESS",
    "lfe": "LFE",
    "liquid": "liquid",
    "lsp": "Lisp",
    "lisp": "Lisp",
    "ll": "LLVM IR",
    "lgt": "Logtalk",
    "logtalk": "Logtalk",
    "wlua": "Lua",
    "rbxs": "Lua",
    "pd_lua": "Lua",
    "p8": "Lua",
    "nse": "Lua",
    "lua": "Lua",
    "m3": "Modula3",
    "m4": "m4",
    "makefile": "make",
    "Makefile": "make",
    "mao": "Mako",
    "mako": "Mako",
    "workbook": "Markdown",
    "ronn": "Markdown",
    "mkdown": "Markdown",
    "mkdn": "Markdown",
    "mkd": "Markdown",
    "mdx": "Markdown",
    "mdwn": "Markdown",
    "mdown": "Markdown",
    "markdown": "Markdown",
    "contents.lr": "Markdown",
    "md": "Markdown",
    "mc": "Windows Message File",
    "met": "Teamcenter met",
    "mg": "Modula3",
    "mojom": "Mojo",
    "meson.build": "Meson",
    "metal": "Metal",
    "mk": "make",
    #           'mli'         : 'ML'                    , # ML not implemented
    #           'ml'          : 'ML'                    ,
    "ml4": "OCaml",
    "eliomi": "OCaml",
    "eliom": "OCaml",
    "ml": "OCaml",
    "mli": "OCaml",
    "mly": "OCaml",
    "mll": "OCaml",
    "m": "MATLAB/Mathematica/Objective-C/MUMPS/Mercury",
    "mm": "Objective-C++",
    "msg": "Gencat NLS",
    "nbp": "Mathematica",
    "mathematica": "Mathematica",
    "ma": "Mathematica",
    "cdf": "Mathematica",
    "mt": "Mathematica",
    "wl": "Mathematica",
    "wlt": "Mathematica",
    "mustache": "Mustache",
    "wdproj": "MSBuild script",
    "csproj": "MSBuild script",
    "vcproj": "MSBuild script",
    "wixproj": "MSBuild script",
    "btproj": "MSBuild script",
    "msbuild": "MSBuild script",
    "ixx": "Visual Studio Module",
    "sln": "Visual Studio Solution",
    "mps": "MUMPS",
    "mth": "Teamcenter mth",
    "n": "Nemerle",
    "nims": "Nim",
    "nimrod": "Nim",
    "nimble": "Nim",
    "nim.cfg": "Nim",
    "nim": "Nim",
    "nix": "Nix",
    "nut": "Squirrel",
    "odin": "Odin",
    "oscript": "LiveLink OScript",
    "bod": "Oracle PL/SQL",
    "spc": "Oracle PL/SQL",
    "fnc": "Oracle PL/SQL",
    "prc": "Oracle PL/SQL",
    "trg": "Oracle PL/SQL",
    "pad": "Ada",  # Oracle Ada preprocessor
    "page": "Visualforce Page",
    "pas": "Pascal",
    "pcc": "C++",  # Oracle C++ preprocessor
    "rexfile": "Perl",
    "psgi": "Perl",
    "ph": "Perl",
    "makefile.pl": "Perl",
    "cpanfile": "Perl",
    "al": "Perl",
    "ack": "Perl",
    "perl": "Perl",
    "pfo": "Fortran 77",
    "pgc": "C",  # Postgres embedded C/C++
    "phpt": "PHP",
    "phps": "PHP",
    "phakefile": "PHP",
    "ctp": "PHP",
    "aw": "PHP",
    "php_cs.dist": "PHP",
    "php_cs": "PHP",
    "php3": "PHP",
    "php4": "PHP",
    "php5": "PHP",
    "php": "PHP",
    "phtml": "PHP",
    "pig": "Pig Latin",
    "plh": "Perl",
    "pl": "Perl/Prolog",
    "PL": "Perl/Prolog",
    "p6": "Raku/Prolog",
    "P6": "Raku/Prolog",
    "plx": "Perl",
    "pm": "Perl",
    "pm6": "Raku",
    "raku": "Raku",
    "rakumod": "Raku",
    "pom.xml": "Maven",
    "pom": "Maven",
    "yap": "Prolog",
    "prolog": "Prolog",
    "P": "Prolog",
    "p": "Pascal",
    "pp": "Pascal/Puppet",
    "viw": "SQL",
    "udf": "SQL",
    "tab": "SQL",
    "mysql": "SQL",
    "cql": "SQL",
    "psql": "SQL",
    "xpy": "Python",
    "wsgi": "Python",
    "wscript": "Python",
    "workspace": "Python",
    "tac": "Python",
    "snakefile": "Python",
    "sconstruct": "Python",
    "sconscript": "Python",
    "pyt": "Python",
    "pyp": "Python",
    "pyi": "Python",
    "pyde": "Python",
    "py3": "Python",
    "lmi": "Python",
    "gypi": "Python",
    "gyp": "Python",
    "build.bazel": "Python",
    "buck": "Python",
    "gclient": "Python",
    "py": "Python",
    "pyw": "Python",
    "ipynb": "Jupyter Notebook",
    "pyj": "RapydScript",
    "pxi": "Cython",
    "pxd": "Cython",
    "pyx": "Cython",
    "qbs": "QML",
    "qml": "QML",
    "watchr": "Ruby",
    "vagrantfile": "Ruby",
    "thorfile": "Ruby",
    "thor": "Ruby",
    "snapfile": "Ruby",
    "ru": "Ruby",
    "rbx": "Ruby",
    "rbw": "Ruby",
    "rbuild": "Ruby",
    "rabl": "Ruby",
    "puppetfile": "Ruby",
    "podfile": "Ruby",
    "mspec": "Ruby",
    "mavenfile": "Ruby",
    "jbuilder": "Ruby",
    "jarfile": "Ruby",
    "guardfile": "Ruby",
    "god": "Ruby",
    "gemspec": "Ruby",
    "gemfile.lock": "Ruby",
    "gemfile": "Ruby",
    "fastfile": "Ruby",
    "eye": "Ruby",
    "deliverfile": "Ruby",
    "dangerfile": "Ruby",
    "capfile": "Ruby",
    "buildfile": "Ruby",
    "builder": "Ruby",
    "brewfile": "Ruby",
    "berksfile": "Ruby",
    "appraisals": "Ruby",
    "pryrc": "Ruby",
    "irbrc": "Ruby",
    "rb": "Ruby",
    "podspec": "Ruby",
    "rake": "Ruby",
    #  'resx'        : 'ASP.NET'               ,
    "rex": "Oracle Reports",
    "pprx": "Rexx",
    "rexx": "Rexx",
    "rhtml": "Ruby HTML",
    "rs.in": "Rust",
    "rs": "Rust",
    "rst.txt": "reStructuredText",
    "rest.txt": "reStructuredText",
    "rest": "reStructuredText",
    "rst": "reStructuredText",
    "s": "Assembly",
    "S": "Assembly",
    "SCA": "Visual Fox Pro",
    "sca": "Visual Fox Pro",
    "sbt": "Scala",
    "kojo": "Scala",
    "scala": "Scala",
    "sbl": "Softbridge Basic",
    "SBL": "Softbridge Basic",
    "sed": "sed",
    "ses": "Patran Command Language",
    "sp": "SparForte",
    "sol": "Solidity",
    "pcl": "Patran Command Language",
    "pl1": "PL/I",
    "plm": "PL/M",
    "lit": "PL/M",
    "puml": "PlantUML",
    "properties": "Properties",
    "po": "PO File",
    "pbt": "PowerBuilder",
    "sra": "PowerBuilder",
    "srf": "PowerBuilder",
    "srm": "PowerBuilder",
    "srs": "PowerBuilder",
    "sru": "PowerBuilder",
    "srw": "PowerBuilder",
    "jade": "Pug",
    "pug": "Pug",
    "purs": "PureScript",
    "prefab": "Unity-Prefab",
    "proto": "Protocol Buffers",
    "mat": "Unity-Prefab",
    "ps1": "PowerShell",
    "psd1": "PowerShell",
    "psm1": "PowerShell",
    "rsx": "R",
    "rd": "R",
    "expr-dist": "R",
    "rprofile": "R",
    "R": "R",
    "r": "R",
    "raml": "RAML",
    "ring": "Ring",
    "rh": "Ring",
    "rform": "Ring",
    "rktd": "Racket",
    "rkt": "Racket",
    "rktl": "Racket",
    "Rmd": "Rmd",
    "re": "ReasonML",
    "rei": "ReasonML",
    "res": "ReScript",
    "resi": "ReScript",
    "scrbl": "Racket",
    "sps": "Scheme",
    "sc": "Scheme",
    "ss": "Scheme",
    "scm": "Scheme",
    "sch": "Scheme",
    "sls": "Scheme/SaltStack",
    "sld": "Scheme",
    "robot": "RobotFramework",
    "rc": "Windows Resource File",
    "rc2": "Windows Resource File",
    "sas": "SAS",
    "sass": "Sass",
    "scss": "SCSS",
    "sh": "Bourne Shell",
    "smarty": "Smarty",
    "sml": "Standard ML",
    "sig": "Standard ML",
    "fun": "Standard ML",
    "slim": "Slim",
    "e": "Specman e",
    "sql": "SQL",
    "SQL": "SQL",
    "sproc.sql": "SQL Stored Procedure",
    "spoc.sql": "SQL Stored Procedure",
    "spc.sql": "SQL Stored Procedure",
    "udf.sql": "SQL Stored Procedure",
    "data.sql": "SQL Data",
    "sss": "SugarSS",
    "st": "Smalltalk",
    "styl": "Stylus",
    "i": "SWIG",
    "svelte": "Svelte",
    "sv": "Verilog-SystemVerilog",
    "svh": "Verilog-SystemVerilog",
    "svg": "SVG",
    "SVG": "SVG",
    "v": "Verilog-SystemVerilog/Coq",
    "td": "TableGen",
    "tcl": "Tcl/Tk",
    "tcsh": "C Shell",
    "tk": "Tcl/Tk",
    "mkvi": "TeX",
    "mkiv": "TeX",
    "mkii": "TeX",
    "ltx": "TeX",
    "lbx": "TeX",
    "ins": "TeX",
    "cbx": "TeX",
    "bib": "TeX",
    "bbx": "TeX",
    "aux": "TeX",
    "tex": "TeX",  # TeX, LaTex, MikTex, ..
    "toml": "TOML",
    "sty": "TeX",
    #           'cls'         : 'TeX'                   ,
    "dtx": "TeX",
    "bst": "TeX",
    "tres": "Godot Resource",
    "tscn": "Godot Scene",
    "thrift": "Thrift",
    "tpl": "Smarty",
    "trigger": "Apex Trigger",
    "ttcn": "TTCN",
    "ttcn2": "TTCN",
    "ttcn3": "TTCN",
    "ttcnpp": "TTCN",
    "sdl": "TNSDL",
    "ssc": "TNSDL",
    "sdt": "TNSDL",
    "spd": "TNSDL",
    "sst": "TNSDL",
    "rou": "TNSDL",
    "cin": "TNSDL",
    "cii": "TNSDL",
    "interface": "TNSDL",
    "in1": "TNSDL",
    "in2": "TNSDL",
    "in3": "TNSDL",
    "in4": "TNSDL",
    "inf": "TNSDL",
    "tpd": "TITAN Project File Information",
    "ts": "TypeScript/Qt Linguist",
    "tsx": "TypeScript",
    "tss": "Titanium Style Sheet",
    "twig": "Twig",
    "um": "Umka",
    "ui": "Qt/Glade",
    "glade": "Glade",
    "vala": "Vala",
    "vapi": "Vala Header",
    "vhw": "VHDL",
    "vht": "VHDL",
    "vhs": "VHDL",
    "vho": "VHDL",
    "vhi": "VHDL",
    "vhf": "VHDL",
    "vhd": "VHDL",
    "VHD": "VHDL",
    "vhdl": "VHDL",
    "VHDL": "VHDL",
    "bas": "Visual Basic",
    "BAS": "Visual Basic",
    "ctl": "Visual Basic",
    "dsr": "Visual Basic",
    "frm": "Visual Basic",
    "frx": "Visual Basic",
    "FRX": "Visual Basic",
    "vba": "VB for Applications",
    "VBA": "VB for Applications",
    "vbhtml": "Visual Basic",
    "VBHTML": "Visual Basic",
    "vbproj": "Visual Basic .NET",
    "vbp": "Visual Basic",  # .vbp - autogenerated
    "vbs": "Visual Basic Script",
    "VBS": "Visual Basic Script",
    "vb": "Visual Basic .NET",
    "VB": "Visual Basic .NET",
    "vbw": "Visual Basic",  # .vbw - autogenerated
    "vue": "Vuejs Component",
    "webinfo": "ASP.NET",
    "wsdl": "Web Services Description",
    "x": "Logos",
    "xm": "Logos",
    "xpo": "X++",  # Microsoft Dynamics AX 4.0 export format
    "xmi": "XMI",
    "XMI": "XMI",
    "zcml": "XML",
    "xul": "XML",
    "xspec": "XML",
    "xproj": "XML",
    "xml.dist": "XML",
    "xliff": "XML",
    "xlf": "XML",
    "xib": "XML",
    "xacro": "XML",
    "x3d": "XML",
    "wsf": "XML",
    "web.release.config": "XML",
    "web.debug.config": "XML",
    "web.config": "XML",
    "wxml": "WXML",
    "wxss": "WXSS",
    "vxml": "XML",
    "vstemplate": "XML",
    "vssettings": "XML",
    "vsixmanifest": "XML",
    "vcxproj": "XML",
    "ux": "XML",
    "urdf": "XML",
    "tmtheme": "XML",
    "tmsnippet": "XML",
    "tmpreferences": "XML",
    "tmlanguage": "XML",
    "tml": "XML",
    "tmcommand": "XML",
    "targets": "XML",
    "sublime-snippet": "XML",
    "sttheme": "XML",
    "storyboard": "XML",
    "srdf": "XML",
    "shproj": "XML",
    "sfproj": "XML",
    "settings.stylecop": "XML",
    "scxml": "XML",
    "rss": "XML",
    "resx": "XML",
    "rdf": "XML",
    "pt": "XML",
    "psc1": "XML",
    "ps1xml": "XML",
    "props": "XML",
    "proj": "XML",
    "plist": "XML",
    "pkgproj": "XML",
    "packages.config": "XML",
    "osm": "XML",
    "odd": "XML",
    "nuspec": "XML",
    "nuget.config": "XML",
    "nproj": "XML",
    "ndproj": "XML",
    "natvis": "XML",
    "mjml": "XML",
    "mdpolicy": "XML",
    "launch": "XML",
    "kml": "XML",
    "jsproj": "XML",
    "jelly": "XML",
    "ivy": "XML",
    "iml": "XML",
    "grxml": "XML",
    "gmx": "XML",
    "fsproj": "XML",
    "filters": "XML",
    "dotsettings": "XML",
    "dll.config": "XML",
    "ditaval": "XML",
    "ditamap": "XML",
    "depproj": "XML",
    "ct": "XML",
    "csl": "XML",
    "csdef": "XML",
    "cscfg": "XML",
    "cproject": "XML",
    "clixml": "XML",
    "ccxml": "XML",
    "ccproj": "XML",
    "builds": "XML",
    "axml": "XML",
    "app.config": "XML",
    "ant": "XML",
    "admx": "XML",
    "adml": "XML",
    "project": "XML",
    "classpath": "XML",
    "xml": "XML",
    "XML": "XML",
    "mxml": "MXML",
    "xml.builder": "builder",
    "build": "NAnt script",
    "vim": "vim script",
    "swift": "Swift",
    "xaml": "XAML",
    "wast": "WebAssembly",
    "wat": "WebAssembly",
    "wxs": "WiX source",
    "wxi": "WiX include",
    "wxl": "WiX string localization",
    "prw": "xBase",
    "prg": "xBase",
    "ch": "xBase Header",
    "xqy": "XQuery",
    "xqm": "XQuery",
    "xql": "XQuery",
    "xq": "XQuery",
    "xquery": "XQuery",
    "xsd": "XSD",
    "XSD": "XSD",
    "xslt": "XSLT",
    "XSLT": "XSLT",
    "xsl": "XSLT",
    "XSL": "XSLT",
    "xtend": "Xtend",
    "yacc": "yacc",
    "y": "yacc",
    "yml.mysql": "YAML",
    "yaml-tmlanguage": "YAML",
    "syntax": "YAML",
    "sublime-syntax": "YAML",
    "rviz": "YAML",
    "reek": "YAML",
    "mir": "YAML",
    "glide.lock": "YAML",
    "gemrc": "YAML",
    "clang-tidy": "YAML",
    "clang-format": "YAML",
    "yaml": "YAML",
    "yml": "YAML",
    "zig": "Zig",
    "zsh": "zsh",
}

CLOC_LANGUAGE_BY_SCRIPT = {
    "awk": "awk",
    "bash": "Bourne Again Shell",
    "bc": "bc",  # calculator
    "crystal": "Crystal",
    "csh": "C Shell",
    "dmd": "D",
    "dtrace": "dtrace",
    "escript": "Erlang",
    "groovy": "Groovy",
    "idl": "IDL",
    "kermit": "Kermit",
    "ksh": "Korn Shell",
    "lua": "Lua",
    "make": "make",
    "octave": "Octave",
    "perl5": "Perl",
    "perl": "Perl",
    "miniperl": "Perl",
    "php": "PHP",
    "php5": "PHP",
    "python": "Python",
    "python2.6": "Python",
    "python2.7": "Python",
    "python3": "Python",
    "python3.3": "Python",
    "python3.4": "Python",
    "python3.5": "Python",
    "python3.6": "Python",
    "python3.7": "Python",
    "python3.8": "Python",
    "perl6": "Raku",
    "raku": "Raku",
    "rakudo": "Raku",
    "rexx": "Rexx",
    "regina": "Rexx",
    "ruby": "Ruby",
    "sed": "sed",
    "sh": "Bourne Shell",
    "swipl": "Prolog",
    "tcl": "Tcl/Tk",
    "tclsh": "Tcl/Tk",
    "tcsh": "C Shell",
    "wish": "Tcl/Tk",
    "zsh": "zsh",
}

CLOC_LANGUAGE_BY_FILE = {
    "build.xml": "Ant/XML",
    "BUILD": "Bazel",
    "WORKSPACE": "Bazel",
    "cmakelists.txt": "CMake",
    "CMakeLists.txt": "CMake",
    "Jamfile": "Jam",
    "jamfile": "Jam",
    "Jamrules": "Jam",
    "Makefile": "make",
    "makefile": "make",
    "meson.build": "Meson",
    "Gnumakefile": "make",
    "gnumakefile": "make",
    "pom.xml": "Maven/XML",
    "Rakefile": "Ruby",
    "rakefile": "Ruby",
    "Dockerfile": "Dockerfile",
    "Dockerfile.m4": "Dockerfile",
    "Dockerfile.cmake": "Dockerfile",
    "dockerfile": "Dockerfile",
    "dockerfile.m4": "Dockerfile",
    "dockerfile.cmake": "Dockerfile",
}
