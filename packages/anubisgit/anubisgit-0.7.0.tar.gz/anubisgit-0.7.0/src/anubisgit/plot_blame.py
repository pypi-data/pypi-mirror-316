"""Analyses from the blame DDB"""

from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

from tol_colors import tol_cmap

# import numpy as np
from anubisgit.data_loader import load_jsons, load_tags, anubisgit_date, load_authors
from anubisgit.datetime_tools import date_merge_semester, timedelta_merge
from anubisgit.timegraph import AnubisTimeGraph
from anubisgit.plot_common import (
    gather_data_by_category,
    create_stack_plot_xbaseline,
    merge_data_with_baseline,
    sort_by_highest_amount,
    stack_data,
)


def gather_by_age(joined_blame: dict, by_age: bool = True) -> dict:
    """
    Gather info on year-month of last edition.

    Note:
        by_age or by birth, the categories amounts are not the same
        As the tranlation is not simple, the switch is in this function.
        A smarter implementation would be heavier...

        { -date-of-observation-1-(datetime) :
            {
                -date-of-last-edit-1-(datetime) : 12,
                -date-of-last-edit-2-(datetime) : 2,

            },
         -date-of-observation-2-(datetime) : {
            (...)
        }

    Args:
        joined_blame (dict): Dict of loaded blame.json
        by_age (bool,optionnal): If true info is the age of code instead of the bith date. Defaults to True

    Returns :
        (dict): LOC ages
    """
    out = {}
    for date, blame_all_files in joined_blame.items():
        out[date] = {}
        for blame_file in blame_all_files:
            for last_edit in blame_file["date"]:
                if by_age:
                    cat_key = timedelta_merge(date - anubisgit_date(last_edit))
                else:
                    cat_key = date_merge_semester(anubisgit_date(last_edit))
                if cat_key not in out[date]:
                    out[date][cat_key] = 0
                out[date][cat_key] += 1
    return out


def gather_by_author(joined_blame: dict, authors: dict) -> dict:
    """
    Gather info on year-month of last edition.

    Args:
        joined_blame (dict): dict of loaded blame.json
        authors (dict): dict with the authors associated with their trigram.

    Returns :
        dict : last edition date of corresponding file
    """

    out = {}

    for date, blame_all_files in joined_blame.items():
        out[date] = {}
        for blame_file in blame_all_files:
            for author in blame_file["author"]:
                try:
                    trigram = authors[author.lower()]
                except KeyError:
                    trigram = "XXX"

                if trigram not in out[date]:
                    out[date][trigram] = 0
                out[date][trigram] += 1
    return out


def plot_birth(
    folder: str = "./",
    date_start: str = None,
    date_end: str = None,
    by_age: bool = True,
) -> plt.Axes:
    """
    Plot the age of the code.

    Args:
        folder (str ,optionnal): Folder where the blame.json is. Defaults to "./"
        date_start (str, optionnal): Starting date. Defaults to None
        date_end (str, optionnal): Ending date. Defaults to None
        by_age (bool, optionnal): Plot data by age. Defaults to True

    Returns:
        plt.Axes: Anubs Timegraph Axes object
    """
    data_by_obs_date = gather_by_age(
        load_jsons(folder, "blame.json", date_start=date_start, date_end=date_end),
        by_age=by_age,
    )

    data_by_cat = gather_data_by_category(data_by_obs_date)

    if by_age:
        title = "Code lines gathered by time since last edition"
        cmap = tol_cmap("YlOrBr")
        annotate = False
        show_legend = True
    else:
        title = "Code lines gathered by date of last edition"
        cmap = tol_cmap("iridescent")
        annotate = True
        show_legend = False

    data_base = create_stack_plot_xbaseline(data_by_cat, "dates")
    homogenous_db = merge_data_with_baseline(data_by_cat, data_base, "dates", "amount")

    worst_candidates = sort_by_highest_amount(homogenous_db, "amount")
    cumulative_data = stack_data(data_base, homogenous_db, "amount")

    abt = AnubisTimeGraph(title)
    abt.create_stackplot(data_base, cumulative_data, cmap=cmap, show_legend=show_legend)
    abt.add_tags(load_tags(folder))
    abt.ax.set_ylim(0, None)
    abt.ax.set_ylabel(f"Lines of code", fontsize=20, rotation=0)
    abt.ax.yaxis.set_label_coords(0.0, 1.02)

    # Annotation for 10 worst
    if annotate:
        abt.add_brackets_val(cumulative_data, worst_candidates)

    return abt.ax


def plot_ownership(
    folder: str = "./",
    date_start: str = None,
    date_end: str = None,
) -> plt.Axes:
    """
    Plot ownership of the code

    Args:
        folder (str, optional): Location of the blame.json. Defaults to "./".
        date_start (str, optional): Starting date. Defaults to None.
        date_end (str, optional): Ending date. Defaults to None.

    Returns:
        plt.Axes: Anubs Timegraph Axes object
    """
    data_by_obs_date = gather_by_author(
        load_jsons(folder, "blame.json", date_start=date_start, date_end=date_end),
        load_authors(folder),
    )
    data_by_cat = gather_data_by_category(data_by_obs_date)
    data_base = create_stack_plot_xbaseline(data_by_cat, "dates")
    homogenous_db = merge_data_with_baseline(data_by_cat, data_base, "dates", "amount")
    worst_candidates = sort_by_highest_amount(homogenous_db, "amount")
    cumulative_data = stack_data(data_base, homogenous_db, "amount")

    cset = cm.get_cmap("tab20")
    abt = AnubisTimeGraph(title=f"Code ownership")
    abt.create_stackplot(
        data_base,
        cumulative_data,
        key_to_color=list(worst_candidates.keys()),
        cmap=cset,
    )
    abt.ax.set_ylabel(f"Lines of code", fontsize=20, rotation=0)
    abt.ax.yaxis.set_label_coords(0.0, 1.02)
    abt.add_tags(load_tags(folder))
    abt.ax.set_ylim(0, None)

    # Annotation for 10 worst
    abt.add_brackets_val(cumulative_data, worst_candidates, display_key=True)

    return abt.ax
