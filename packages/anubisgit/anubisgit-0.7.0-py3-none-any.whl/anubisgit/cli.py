#!/usr/bin/env python
"""
cli.py

Command line interface for tools in Anubis
"""
import click
import anubisgit
from loguru import logger

from anubisgit.plot_complexity import GLOBAL_COMPLEXITY_METRICS

# pylint: disable=import-outside-toplevel

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
DPCTD = "Deprecated command from python package oms..."


def add_version(f):
    """
    Add the version of the tool to the help heading.
    :param f: function to decorate
    :return: decorated function
    """
    doc = f.__doc__
    f.__doc__ = (
        "Package " + anubisgit.__name__ + " v" + anubisgit.__version__ + "\n\n" + doc
    )

    return f


@click.group()
@add_version
def main_cli():
    """
                       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡇⠀⢠⣾⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⡇⢠⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⢸⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⡀⠙⠛⠃⠘⠻⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                       ⠀⠀⠀⠀⠀⠀⠀⠐⠚⣛⣛⣁⡀⠹⣿⣿⣶⣶⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                       ⠀⠀⠀⠀⣠⣴⠶⠿⠛⠛⠛⠛⠛⠀⢻⣿⣿⣤⣀⣙⣷⣀⠀⠀⠀⠀⠀⠀⠀⠀
                       ⠀⠀⠀⣈⣁⣤⣴⣶⠶⠿⠿⠿⠿⠇⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣤⡄⠀
                       ⠀⠀⠐⠛⢉⣉⣠⣤⣤⣶⣶⣶⣶⣦⠀⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠛⠉⠀⠀
                       ⠀⠀⡾⠛⠉⠉⠉⠙⠻⢿⣿⣿⣿⣿⡀⢹⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                       ⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⡇⠘⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                       ⠀⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⡇⠀⣾⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠃⠀⢿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⠀⠀⠸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠀⠀⠀⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

    ---------------------------  AnubisGit  ----------------------------

    You are now using the Command line interface of anubisgit package,
    a set of tools created at CERFACS (https://cerfacs.fr).

    This is a python package currently installed in your python environement.
    """
    pass


@click.command()
@click.option(
    "--filename",
    "-f",
    type=str,
    default="./anubis_time_machine.yml",
    help="Input file with custom name (.yml)",
)
def anew(filename="./anubis_time_machine.yml"):
    """Create default input file in current folder."""
    import os, shutil
    from pkg_resources import resource_filename

    write = True
    if os.path.isfile(filename):
        msg = f"File {filename} already exists. Overwrite ? [y/N] "
        if input(msg).lower() == "n":
            write = False
            logger.info("File not created, older exsisting file has been kept.")

    if write:
        logger.info(f"Generating dummy inputfile {filename} for AnubisGit.")
        shutil.copy2(
            resource_filename(__name__, "anubis_time_machine.yml"),
            filename,
        )
        logger.success(
            f"File {filename} created. Edit this file to set up your project..."
        )


main_cli.add_command(anew)


@click.command()
@click.option(
    "--file", "-f", type=str, default=None, help="Input file with a custom name (.yml)"
)
def timemachine(file):
    """Build AnubisGit database

    INPUTFILE.yml defines the parameters of your investigation
    """
    from anubisgit.timemachine import run

    if file:
        run(inputfile=file)
    else:
        run()


main_cli.add_command(timemachine)


@click.command()
@click.argument(
    "anubisgit-out-dir", type=click.Path(exists=True), default=None, nargs=1
)
def join_db(anubisgit_out_dir):
    """Join AnubisGit database

    ANUBIS_OUT_DIR: Anubis database directory.
    """
    from anubisgit.joindb import join_monthly_ddb

    join_monthly_ddb(anubisgit_out_dir)
    logger.success(f"Database are now joined in {anubisgit_out_dir}")


main_cli.add_command(join_db)


@click.command()
@click.argument(
    "anubisgit-out-dir", type=click.Path(exists=True), default=None, nargs=1
)
def authors_list(anubisgit_out_dir):
    """Retrieve authors list from joined_commits_monthly.json

    ANUBIS_OUT_DIR: Anubis database directory.
    """
    import json
    from pathlib import Path
    from anubisgit.authors import get_author_list, build_aliases

    root = Path(anubisgit_out_dir)
    fname = root / "authors_list.json"
    logger.info("This can take a while...")
    with open(fname, "w") as fout:
        json.dump(build_aliases(get_author_list(anubisgit_out_dir)), fout, indent=4)
    logger.success(f"Authors aliases dumped at {fname}.")


main_cli.add_command(authors_list)


@click.command()
@click.argument(
    "anubisgit-out-dir", type=click.Path(exists=True), default=None, nargs=1
)
@click.option(
    "--viz",
    type=click.Choice(["matplotlib", "plotly"]),
    default="matplotlib",
    help="Visualization backend",
)
@click.option(
    "--ctype",
    "-c",
    type=click.Choice([m for m in GLOBAL_COMPLEXITY_METRICS.keys() if m != "score"]),
    default=None,
    help="Complexity metric to target. If not specified, plot all.",
)
def complexity(anubisgit_out_dir, viz, ctype):
    """Analyse code health

    ANUBIS_OUT_DIR: Anubis database directory.
    """
    from anubisgit.plot_complexity import plot_complexity, plot_worst_performers
    from anubisgit.plot_complexity_html import (
        plot_global_complexity_html,
        plot_worst_performers_html,
    )
    from anubisgit.pyplot_tools import save_this_fig

    if ctype is None:
        ctype = "global"

    if viz == "plotly":
        fig = plot_global_complexity_html(anubisgit_out_dir)
        logger.info(f"Saving {anubisgit_out_dir}/complexity_global.html")
        fig.write_html(
            f"{anubisgit_out_dir}//complexity_global.html",
            full_html=False,
            include_plotlyjs="cdn",
        )
        fig = plot_worst_performers_html(anubisgit_out_dir)
        logger.info(f"Saving {anubisgit_out_dir}/complexity_worst_performers.html")
        fig.write_html(
            f"{anubisgit_out_dir}/complexity_worst_performers.html",
            full_html=False,
            include_plotlyjs="cdn",
        )
    else:
        plot_complexity(anubisgit_out_dir, ctype)
        save_this_fig(f"complexity_{ctype}.svg", anubisgit_out_dir, width=20, height=15)
        plot_worst_performers(anubisgit_out_dir)
        save_this_fig(
            "complexity_worst_performers.svg", anubisgit_out_dir, width=20, height=15
        )


main_cli.add_command(complexity)


@click.command()
@click.argument(
    "anubisgit-out-dir", type=click.Path(exists=True), default=None, nargs=1
)
@click.option(
    "--exclude_patterns",
    type=str,
    default=None,
    help="list of patterns to exclude from the branches lists",
)
@click.option(
    "--viz",
    type=click.Choice(["matplotlib", "plotly"]),
    default="matplotlib",
    help="Visualization backend",
)
def branches(anubisgit_out_dir, exclude_patterns, viz):
    """Analyze branch health

    ANUBIS_OUT_DIR: Anubis database directory.
    """
    from anubisgit.plot_branches import plot_worst_performers, plot_all_ahead
    from anubisgit.plot_branches_html import (
        plot_global_branches_html,
        plot_worst_branches_html,
    )
    from anubisgit.pyplot_tools import save_this_fig

    if exclude_patterns:
        exclude_patterns = exclude_patterns.split(",")
    else:
        exclude_patterns = []

    if viz == "plotly":
        fig = plot_worst_branches_html(
            anubisgit_out_dir, exclude_patterns=exclude_patterns
        )
        logger.info(f"Saving {anubisgit_out_dir}/branches_worst_behind.html\n")
        fig.write_html(
            f"{anubisgit_out_dir}/branches_worst_behind.html",
            full_html=False,
            include_plotlyjs="cdn",
        )

        fig = plot_worst_branches_html(
            anubisgit_out_dir, ctype="ahead", exclude_patterns=exclude_patterns
        )
        logger.info(f"Saving {anubisgit_out_dir}/branches_worst_ahead.html\n")
        fig.write_html(
            f"{anubisgit_out_dir}/branches_worst_ahead.html",
            full_html=False,
            include_plotlyjs="cdn",
        )

        fig = plot_global_branches_html(
            anubisgit_out_dir, switch_behind=False, exclude_patterns=exclude_patterns
        )
        logger.info(f"Saving {anubisgit_out_dir}/branches_all_ahead.html\n")
        fig.write_html(
            f"{anubisgit_out_dir}/branches_all_ahead.html",
            full_html=False,
            include_plotlyjs="cdn",
        )

        fig = plot_global_branches_html(
            anubisgit_out_dir, exclude_patterns=exclude_patterns
        )
        logger.info(f"Saving {anubisgit_out_dir}/branches_all_behind.html\n")
        fig.write_html(
            f"{anubisgit_out_dir}/branches_all_behind.html",
            full_html=False,
            include_plotlyjs="cdn",
        )

    else:
        plot_worst_performers(
            anubisgit_out_dir, switch_behind=True, exclude_patterns=exclude_patterns
        )
        save_this_fig(
            "branches_worst_behind.svg", anubisgit_out_dir, width=30, height=25
        )

        plot_worst_performers(
            anubisgit_out_dir, switch_behind=False, exclude_patterns=exclude_patterns
        )
        save_this_fig(
            "branches_worst_ahead.svg", anubisgit_out_dir, width=30, height=25
        )

        plot_all_ahead(anubisgit_out_dir, exclude_patterns=exclude_patterns)
        save_this_fig("branches_all_ahead.svg", anubisgit_out_dir, width=20, height=15)


main_cli.add_command(branches)


@click.command()
@click.argument(
    "anubisgit-out-dir", type=click.Path(exists=True), default=None, nargs=1
)
@click.option(
    "--viz",
    type=click.Choice(["matplotlib", "plotly"]),
    default="matplotlib",
    help="Visualization backend",
)
def chronology(anubisgit_out_dir, viz):
    """
    Code geology

    ANUBIS_OUT_DIR: Anubis database directory.
    """
    from anubisgit.plot_blame import plot_ownership, plot_birth
    from anubisgit.plot_blame_html import plot_ownership_html, plot_birth_html
    from anubisgit.pyplot_tools import save_this_fig

    if viz == "plotly":
        fig = plot_ownership_html(anubisgit_out_dir)
        logger.info(f"Saving {anubisgit_out_dir}/chrono_ownership.html\n")
        fig.write_html(
            f"{anubisgit_out_dir}/chrono_ownership.html",
            full_html=False,
            include_plotlyjs="cdn",
        )

        fig = plot_birth_html(anubisgit_out_dir, by_age=False)
        logger.info(f"Saving {anubisgit_out_dir}/chrono_birth.html\n")
        fig.write_html(
            f"{anubisgit_out_dir}/chrono_birth.html",
            full_html=False,
            include_plotlyjs="cdn",
        )

        fig = plot_birth_html(anubisgit_out_dir, by_age=True)
        logger.info(f"Saving {anubisgit_out_dir}/chrono_age.html\n")
        fig.write_html(
            f"{anubisgit_out_dir}/chrono_age.html",
            full_html=False,
            include_plotlyjs="cdn",
        )

    else:
        plot_ownership(anubisgit_out_dir)
        save_this_fig("chrono_ownership.svg", anubisgit_out_dir, width=20, height=15)
        plot_birth(anubisgit_out_dir, by_age=False)
        save_this_fig("chrono_birth.svg", anubisgit_out_dir, width=20, height=15)
        plot_birth(anubisgit_out_dir, by_age=True)
        save_this_fig("chrono_age.svg", anubisgit_out_dir, width=20, height=15)


main_cli.add_command(chronology)


@click.command()
@click.argument(
    "anubisgit-out-dir", type=click.Path(exists=True), default=None, nargs=1
)
@click.option(
    "--authors",
    "-a",
    multiple=True,
    type=str,
    default=["all"],
    help="Name of the authors to analyze the activity",
)
def activity(anubisgit_out_dir, authors):
    """Activity observed on the repository

    ANUBIS_OUT_DIR: Anubis database directory.
    """
    from anubisgit.plot_activity import (
        plot_activity_cumulated,
        plot_activity_authors,
        # plot_activity_additions,
        plot_global_additions,
        plot_commit_activity,
    )
    from anubisgit.pyplot_tools import save_this_fig

    plot_activity_cumulated(
        "date",
        "additions",
        "Authors Cumulated Additions",
        "Cumulated Additions",
        folder=anubisgit_out_dir,
        authors_list=authors,
    )
    save_this_fig("activity_additions_date.svg", anubisgit_out_dir, width=20, height=15)
    plot_activity_cumulated(
        "date",
        "commits_days",
        "Authors Cumulated Commit Days",
        "Cumulated Commit Days",
        folder=anubisgit_out_dir,
        authors_list=authors,
    )
    save_this_fig(
        "activity_commitdays_date.svg", anubisgit_out_dir, width=20, height=15
    )
    plot_activity_cumulated(
        "age",
        "commits_days",
        "Authors Cumulated Commit Days",
        "Cumulated Commit Days",
        xlabel="Experience in months",
        folder=anubisgit_out_dir,
        authors_list=authors,
    )
    save_this_fig("activity_commitdays_age.svg", anubisgit_out_dir, width=20, height=15)

    plot_activity_authors(
        "time",
        "auth",
        "Number of disctinct authors",
        folder=anubisgit_out_dir,
        authors_list=authors,
    )
    save_this_fig("activity_authorsmonth.svg", anubisgit_out_dir, width=20, height=15)

    # plot_activity_additions(
    #     "time",
    #     "additions",
    #     "Test additions",
    #     folder=anubisgit_out_dir,
    #     authors_list=authors,
    # )
    # save_this_fig("activity_additionsmonth.svg", anubisgit_out_dir, width=20, height=15)

    plot_global_additions(folder=anubisgit_out_dir, authors_list=authors)
    save_this_fig(
        "activity_global_addition_rate.svg",
        anubisgit_out_dir=anubisgit_out_dir,
        width=20,
        height=15,
    )
    plot_commit_activity(folder=anubisgit_out_dir)
    save_this_fig(
        "activity_commits_on_branch.svg",
        anubisgit_out_dir=anubisgit_out_dir,
        width=20,
        height=15,
    )


main_cli.add_command(activity)


@click.command()
@click.option(
    "--file", "-f", type=str, default=None, help="Input file with a custom name (.yml)"
)
def analyze_branches(file):
    """Analyze all branches in repository.

    WARNING : Run a timemachine's timeloop - can be long.
    INPUTFILE.yml defines the parameters of your investigation
    """
    from anubisgit.timemachine import run_timemachine_for_branch_analysis
    from anubisgit.plot_branches import (
        plot_commit_activity_by_branch,
        plot_branch_activity_state,
    )
    from anubisgit.pyplot_tools import save_this_fig
    import yaml

    if file:
        run_timemachine_for_branch_analysis(inputfile=file)
    else:
        run_timemachine_for_branch_analysis()

    if file is None:
        file = "./anubis_time_machine.yml"

    with open(file, "r") as fin:
        param = yaml.load(fin, Loader=yaml.SafeLoader)

    out_dir = param.get("out_dir")

    plot_commit_activity_by_branch(out_dir)
    save_this_fig("commit_activity_by_branch.svg", out_dir, width=30, height=25)

    plot_branch_activity_state(out_dir)
    save_this_fig("branch_actitivy_state.svg", out_dir, width=20, height=15)


main_cli.add_command(analyze_branches)
