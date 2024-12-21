"""Module able to spawn several temporal versions of a git codebase"""

import json
import os
import subprocess
from typing import List, Union

from datetime import datetime, timedelta
from time import time

import yaml
from dateutil.relativedelta import relativedelta
from loguru import logger

from tucan.travel_in_package import find_package_files_and_folders
from tucan.package_analysis import run_struct

from anubisgit.external_analysis import rearrange_tucan_complexity_db
from anubisgit.git_helpers import (
    git_blame,
    git_branch_status,
    git_checkout,
    git_last_revision,
    git_revision_in_between,
    git_revision_stats,
    git_tag_history,
    git_size,
    git_merge_branch,
)


def timeloop(
    path: str,
    branch: str,
    year_start: int,
    year_end: int,
    out_dir: str,
    mandatory_patterns: List[str] = None,
    forbidden_patterns: List[str] = None,
) -> None:
    """
    Principal time loop for anubisgit.

    Args :
        path (str): Path relative to git repo to limit the results.
        branch (str): Git branch to scan.
        year_start (int): Starting year, included.
        year_end (int): Ending year, included.
        out_dir (str): Output directory.
        mandatory_patterns (List[str], optionnal): List of patterns to keep. Defaults to None.
        forbidden_patterns (List[str], optionnal): List of patterns to remove. Defaults to None.
    """
    total = (year_end - year_start + 1) * 12
    step = 0
    for year in range(year_start, year_end + 1):
        for month in range(12):
            raw_date = datetime(year, month + 1, 1, 12, 0)
            raw_date_m1 = raw_date + relativedelta(months=-1)
            if raw_date >= datetime.today():
                logger.info("Timemachine won't go in the future ... Stopping there")
                break

            logger.info(f"{year}-{month + 1}")
            tstart = time()
            step += 1

            folder = f"{out_dir}/anubisgit_{year}-{month+1:02d}"
            if os.path.isdir(folder):
                continue

            os.makedirs(folder)
            logger.info(f"Creating folder : {folder}")
            logger.info(
                f"Timewarping ({step}/{total})... Date is now {raw_date.isoformat()}"
            )

            process_month(
                path,
                branch,
                folder,
                raw_date.isoformat(),
                raw_date_m1.isoformat(),
                mandatory_patterns,
                forbidden_patterns,
            )
            tend = time()
            duration = tend - tstart
            eta = timedelta(seconds=(total - step) * duration)
            logger.info(f"ETA: {eta} sec")

    # Back to now
    subprocess.run(["git", "checkout", branch])

    # tag history
    tags_date = git_tag_history(branch)
    write_json(f"{folder}/../tags_history.json", tags_date)


def process_month(
    path: str,
    branch: str,
    folder: str,
    date: str,
    date_m1: str,
    mandatory_patterns: List[str],
    forbidden_patterns: List[str],
) -> None:
    """
    Processes data for a single month.

    Args:
        path (str): Path relative to git repo to limit the results.
        branch (str): Main branch name.
        folder (str): Folder in which the files are stored for current month
        date (str): First day of the month.
        date_m1 (str): First day of the month before.
        mandatory_patterns (List[str]): List of patterns to keep.
        forbidden_patterns (List[str]): List of patterns to remove.
    """
    revision = git_last_revision(date, branch)
    if revision is None:
        logger.warning(f"No revision found for {date} on branch {branch}. Skipping.")
        return

    # Checkout commit
    git_checkout(revision)

    # Checking path / file
    new_paths = find_package_files_and_folders(
        path, mandatory_patterns, forbidden_patterns
    )
    if not new_paths:
        logger.warning(
            f"No valid files or folders found for {date}. Skipping month processing."
        )
        return

    # Commits info
    revision_list_main = git_revision_in_between(date_m1, date, branch=branch)
    revision_list_all = git_revision_in_between(date_m1, date)
    rev_stats = git_revision_stats(branch, revision_list_main, revision_list_all)
    write_json(f"{folder}/commits.json", rev_stats)

    # Analyze package files
    logger.info("... running tucan")
    tucan_struct = run_struct(new_paths, ignore_errors=True)
    tucan_out = rearrange_tucan_complexity_db(tucan_struct)
    write_json(f"{folder}/complexity.json", tucan_out)

    # Blame info
    blame_info = git_blame(list(new_paths.keys()))
    write_json(f"{folder}/blame.json", blame_info)

    # Branch analysis
    branch_info = git_branch_status(revision, date, branch)
    write_json(f"{folder}/branch_status.json", branch_info)

    # Repo size in bytes
    gitsize = git_size(list(new_paths.keys()))
    write_json(f"{folder}/git_size.json", {"size": gitsize})


def main_timemachine(
    git_path: str,
    branch: str = "master",
    year_start: int = 2020,
    year_end: int = 2020,
    out_dir: str = "ANUBIS_OUT",
    mandatory_patterns: List[str] = None,
    forbidden_patterns: List[str] = None,
) -> None:
    """
    Main call of timemachine

    Args :
        git_path (str): Path to git repository
        branch (str, optionnal): Git branch to scan. Defaults to "master".
        year_start (int, optionnal): Starting year, included. Defaults to 2020.
        year_end (int, optionnal): Ending year, included. Defaults to 2020.
        out_dir (str, optionnal): Output directory. Defaults to "ANUBIS_OUT".
        mandatory_patterns (List[str], optionnal): List of patterns to keep. Defaults to None.
        forbidden_patterns (List[str], optionnal): List of patterns to remove. Defaults to None.
    """

    init_path = os.path.abspath(os.getcwd())
    full_dir = os.path.join(init_path, out_dir)

    if os.path.isdir(full_dir):
        pass
    else:
        os.makedirs(full_dir)

    f_log = os.path.join(init_path, out_dir, f"anubisgit_{os.getpid()}.log")
    logger.info(f_log)

    logger.info(full_dir)
    os.chdir(git_path)
    logger.info(f"Changing cwdir to {git_path} ")

    # Check if repo is clean before running timeloop
    sp = subprocess.run(["git", "status", "--porcelain"], capture_output=True)
    if not sp.stdout.decode():
        # repo is clean = stdout is empty
        timeloop(
            git_path,
            branch,
            year_start,
            year_end,
            full_dir,
            mandatory_patterns=mandatory_patterns,
            forbidden_patterns=forbidden_patterns,
        )
        os.chdir(init_path)

        logger.info(f"Run log stored in {f_log} ")
    else:
        logger.error(f"error: Git repository is not clean:")
        logger.error(sp.stdout.decode())
        logger.error(
            f"Please, commit your changes or stash them before you can use Anubis timemachine.\nAborting"
        )


def run(inputfile="./anubisgit_time_machine.yml") -> None:
    """
    Run anubisgit time machine from input file.

    Args:
        inputfile (str, optional): Path and name to the inputfile. Defaults to "./anubisgit_time_machine.yml".

    """
    logger.info(f"Start anubisgit from command line on {inputfile}\n")

    try:
        with open(inputfile, "r") as fin:
            param = yaml.load(fin, Loader=yaml.SafeLoader)
    except FileNotFoundError:
        logger.error(
            f'Input file {inputfile} not found, use the command "anubisgit anew" to create a new one'
        )
        raise

    main_timemachine(**param)


def timeloop_for_br_analysis(
    path: str,
    branch: str,
    year_start: int,
    year_end: int,
    out_dir: str,
    mandatory_patterns: List[str] = None,
    forbidden_patterns: List[str] = None,
) -> None:
    """
    Principal time loop for timemachine for branch analysis.
    Only dump commits json.

    Args :
        path (str): Path relative to git repo to limit the results.
        branch (str): Git branch to scan.
        year_start (int): Starting year, included.
        year_end (int): Ending year, included.
        out_dir (str): Output directory.
        mandatory_patterns (List[str], optionnal): List of patterns to keep. Defaults to None.
        forbidden_patterns (List[str], optionnal): List of patterns to remove. Defaults to None.
    """

    common_commit = git_merge_branch(branch)

    total = (year_end - year_start + 1) * 12
    step = 0
    for year in range(year_start, year_end + 1):
        for month in range(12):
            raw_date = datetime(year, month + 1, 1, 12, 0)
            raw_date_m1 = raw_date + relativedelta(months=-1)
            if raw_date >= datetime.today():
                logger.info("Timemachine won't go in the future ... Stopping there")
                break

            logger.info(f"{year}-{month + 1}")
            tstart = time()
            step += 1

            folder = f"{out_dir}/anubisgit_{year}-{month+1:02d}"
            if not os.path.isdir(folder):
                os.makedirs(folder)
                logger.info(f"Creating folder : {folder}")

            logger.info(
                f"Timewarping ({step}/{total})... Date is now {raw_date.isoformat()}"
            )

            process_commits_for_branch_analysis(
                path,
                branch,
                folder,
                raw_date.isoformat(),
                raw_date_m1.isoformat(),
                common_commit,
                mandatory_patterns,
                forbidden_patterns,
            )

            tend = time()
            duration = tend - tstart
            eta = timedelta(seconds=(total - step) * duration)
            logger.info(f"ETA: {eta} sec")

    # Back to now
    subprocess.run(["git", "checkout", branch])


def process_commits_for_branch_analysis(
    path: str,
    branch: str,
    folder: str,
    date: str,
    date_m1: str,
    common_commit: dict,
    mandatory_patterns: List[str],
    forbidden_patterns: List[str],
) -> None:
    """
    Processes data for a single month for branch analysis.
    Only dump the commits json.

    Args:
        path (str): Path relative to git repo to limit the results.
        branch (str): Main branch name.
        folder (str): Folder in which the files are stored for current month
        date (str): First day of the month.
        date_m1 (str): First day of the month before.
        common_commit (dict): Each branch's commit hash of the most recent common ancestor with dev branch.
        mandatory_patterns (List[str]): List of patterns to keep.
        forbidden_patterns (List[str]): List of patterns to remove.
    """
    revision = git_last_revision(date, branch)
    if revision is None:
        logger.warning(f"No revision found for {date} on branch {branch}. Skipping.")
        return

    # Checkout commit
    git_checkout(revision)

    # Checking path / file
    new_paths = find_package_files_and_folders(
        path, mandatory_patterns, forbidden_patterns
    )
    if not new_paths:
        logger.warning(
            f"No valid files or folders found for {date}. Skipping month processing."
        )
        return

    # Commits info
    revision_list_main = git_revision_in_between(date_m1, date, branch=branch)
    revision_list_all = git_revision_in_between(date_m1, date)
    rev_stats = git_revision_stats(
        branch,
        revision_list_main,
        revision_list_all,
        other_filter=False,
        common_commit=common_commit,
    )
    write_json(f"{folder}/commits_with_br_names.json", rev_stats)


def main_timemachine_for_branch_analysis(
    git_path: str,
    branch: str = "master",
    year_start: int = 2020,
    year_end: int = 2020,
    out_dir: str = "ANUBIS_OUT",
    mandatory_patterns: List[str] = None,
    forbidden_patterns: List[str] = None,
) -> None:
    """
    Main call of timemachine for branch analysis.

    Args :
        git_path (str): Path to git repository
        branch (str, optionnal): Git branch to scan. Defaults to "master".
        year_start (int, optionnal): Starting year, included. Defaults to 2020.
        year_end (int, optionnal): Ending year, included. Defaults to 2020.
        out_dir (str, optionnal): Output directory. Defaults to "ANUBIS_OUT".
        mandatory_patterns (List[str], optionnal): List of patterns to keep. Defaults to None.
        forbidden_patterns (List[str], optionnal): List of patterns to remove. Defaults to None.
    """

    init_path = os.path.abspath(os.getcwd())
    full_dir = os.path.join(init_path, out_dir)

    if os.path.isdir(full_dir):
        pass
    else:
        os.makedirs(full_dir)

    f_log = os.path.join(init_path, out_dir, f"anubisgit_{os.getpid()}.log")
    logger.info(f_log)

    logger.info(full_dir)
    os.chdir(git_path)
    logger.info(f"Changing cwdir to {git_path} ")

    # Check if repo is clean before running timeloop
    sp = subprocess.run(["git", "status", "--porcelain"], capture_output=True)
    if not sp.stdout.decode():
        # repo is clean = stdout is empty
        timeloop_for_br_analysis(
            git_path,
            branch,
            year_start,
            year_end,
            full_dir,
            mandatory_patterns=mandatory_patterns,
            forbidden_patterns=forbidden_patterns,
        )
        os.chdir(init_path)

        logger.info(f"Run log stored in {f_log} ")
    else:
        logger.error(f"error: Git repository is not clean:")
        logger.error(sp.stdout.decode())
        logger.error(
            f"Please, commit your changes or stash them before you can use timemachine for branch analysis.\nAborting"
        )


def run_timemachine_for_branch_analysis(
    inputfile="./anubisgit_time_machine.yml",
) -> None:
    """
    Run anubisgit time machine from input file for branch analysis.

    Args:
        inputfile (str, optional): Path and name to the inputfile. Defaults to "./anubisgit_time_machine.yml".

    """
    logger.info(f"Start anubisgit from command line on {inputfile}\n")

    try:
        with open(inputfile, "r") as fin:
            param = yaml.load(fin, Loader=yaml.SafeLoader)
    except FileNotFoundError:
        logger.error(
            f'Input file {inputfile} not found, use the command "anubisgit anew" to create a new one'
        )
        raise

    main_timemachine_for_branch_analysis(**param)


def write_json(file_path: str, data: Union[dict, list]) -> None:
    """
    Helper function to write JSON data to a file.

    Args:
        file_path (str): Full path and filename in which the data is dumped.
        data (Union[dict,list]) : Either a dict or list with various data from analysis.

    """
    with open(file_path, "w") as fout:
        json.dump(data, fout, indent=4)
