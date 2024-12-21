""" Sort and plot branches data


The data *branches_per_obs_date* is one record per observation date : 
each record being four keys holding a list/nparray of the same length.

.. text

    {
        timedate(2022,6,2): {
            "branch": np.array(str)
            "behind": np.array(int)
            "ahead": np.array(int)
            "nb_commits_ref_branch": np.array(int)  
        },
    }

The data *branches_evolution_data* is one record per branch,
each record being four keys holding a list/nparray of the same length.


.. text

    { "RELEASE/0.7.3":
        "date":  list(datetime)
        "behind":  list(int)
        "ahead": list(int)
        "nb_commits_ref_branch": list(int) 
    }

"""

BRANCHES_KEYS = ["branch", "behind", "ahead", "nb_commits_ref_branch"]


import matplotlib.pyplot as plt
import numpy as np

from tol_colors import tol_cset

from anubisgit.plot_common import (
    create_stack_plot_xbaseline,
    sort_by_highest_amount,
    gather_data_by_category_in_list,
    merge_data_with_baseline,
    stack_data,
)
from anubisgit.data_loader import load_jsons, load_tags
from anubisgit.timegraph import AnubisTimeGraph


def branches_exclude_patterns(
    branches_per_obs_date: dict, exclude_patterns: list = None
) -> dict:
    """
    Filter the branches join dictionnary from exclusion patterns

    Note:
        Final structure

        { timedate(2022,6,2):
            "branch": np.array(str)
            "behind": np.array(int)
            "ahead": np.array(int)
            "nb_commits_ref_branch": np.array(int)

        }

    Args :
        branches_per_obs_date (dict) : Initial data stored by obeservation date, list of dict for each branch at each date.
        exclude_patterns (list, optionnal): Patterns to remove from branches. Defaults to None.

    Returns :
        f_branches (dict): Dict filtered , using nparrays as a final container looks like the one in the docstrings note.


    """
    f_branches = dict()
    for date, branch_list in branches_per_obs_date.items():
        tmp_ = dict()
        for key in BRANCHES_KEYS:
            tmp_[key] = list()

        for branch_d in branch_list:
            included = True
            for pattern in exclude_patterns:
                if pattern in branch_d["branch"]:
                    included = False
            if included:
                for key in BRANCHES_KEYS:
                    tmp_[key].append(branch_d[key])

        f_branches[date] = dict()
        for key in BRANCHES_KEYS:
            f_branches[date][key] = np.array(tmp_[key])
    return f_branches


def branches_as_dicts(
    filtered_branches: dict,
) -> dict:
    """
    Branches as dicts of lists

    Note:
        obs_date-1- {
            {
                "branch": "feature/nob_allclose",
                "behind": 20,
                "ahead": 0,
                "nb_commits_ref_branch": 1828
            },
            {
                "branch": "remotes/origin/1.1",
                "behind": 967,
                "ahead": 2,
                "nb_commits_ref_branch": 1828
            },
        }

    Args:
        filtered_branches (dict) : Dict filtered , using nparrays as a final container, everything gathered.

    Returns:
        dict_branches (dict): Branch name as key, contains number of commits behind, ahead etc
    """

    keys_m1 = [key for key in BRANCHES_KEYS if key not in ["branch"]]

    dict_branches = {}
    for date, dict_ in reversed(filtered_branches.items()):
        for index in range(dict_["branch"].size):
            bname = dict_["branch"][index]
            bname = bname.split("origin/")[-1]

            if bname not in dict_branches:
                # Initialize
                dict_branches[bname] = {
                    "dates": [],
                }
                for key in keys_m1:
                    dict_branches[bname][key] = list()
            # Append
            dict_branches[bname]["dates"].append(date)
            for key in keys_m1:
                dict_branches[bname][key].append(dict_[key][index])

    return dict_branches


def most_delayed_branches(
    branches_per_obs_date: dict,
    cat_key: str,
    qoi_key: str,
    selection_size: int = 10,
) -> dict:
    """
    Select all categories that were amongst the top performer at least one time

    Note:
        Structure output exemple

        { timedate(2022,6,2):
            "branch": np.array(str)
            "behind": np.array(int)
            "ahead": np.array(int)
            "nb_commits_ref_branch": np.array(int)

        }
    Args:
        branches_per_obs_date (dict of dict of lists) : A Two level dict of lists.
        cat_key (str): First lvl key to used find the branch.
        qoi_key (str): The second lvl key used to find max.
        selection_size (int): Nb of top performers to select.

    Returns:
        dict_top10 (dicts): dict of top performers
    """

    dict_top10 = {}
    for date, dict_ in branches_per_obs_date.items():
        qoi = dict_[qoi_key]
        local_max = min(selection_size, qoi.size - 1)
        mask_top10 = np.argpartition(qoi, -local_max)[-local_max:]

        for index in mask_top10:
            name = dict_[cat_key][index]
            if name not in dict_top10:
                dict_top10[name] = {
                    "dates": [],
                    "score": [],
                }
            dict_top10[name]["dates"].append(date)
            dict_top10[name]["score"].append(qoi[index])

    return dict_top10


def plot_worst_performers(
    folder: str = "./",
    switch_behind: bool = True,
    date_start: str = None,
    date_end: str = None,
    nbranches: int = 10,
    exclude_patterns: list = None,
) -> plt.Axes:
    """
    Plot the worst performers in a code for the branch.

    Args:
        folder (str, optional): Emplacement of branch_status.json file. Defaults to "./".
        switch_behind (bool, optional): Look for the worst ahead or behind branches. Defaults to True.
        date_start (str, optional): Starting date. Defaults to None.
        date_end (str, optional): Ending date. Defaults to None.
        nbranches (int, optional): Number of worst branches to show. Defaults to 10.
        exclude_patterns (list, optional): List of patterns in branches name to exclude. Defaults to None.

    Returns:
        plt.Axes: Anubis Timegraph Axes object
    """
    if switch_behind:
        qoi_key = "behind"
    else:
        qoi_key = "ahead"

    branches_per_obs_date = branches_exclude_patterns(
        load_jsons(
            folder, "branch_status.json", date_start=date_start, date_end=date_end
        ),
        exclude_patterns=exclude_patterns,
    )
    data_by_cat = gather_data_by_category_in_list(
        branches_per_obs_date, "branch", qoi_key
    )
    worst_branches = sort_by_highest_amount(data_by_cat, "amount", span="last")

    cset = tol_cset("muted")
    abt = AnubisTimeGraph(title=f"{nbranches} unmerged branches most {qoi_key}")
    abt.create_lineplot(
        data_by_cat,
        "dates",
        "amount",
        cset,
        marker="o",
        specific_candidates=list(worst_branches.keys()),
    )
    abt.ax.set_ylim(0, None)
    abt.ax.set_ylabel(f"Commits {qoi_key}", fontsize=20, rotation=0)
    abt.ax.yaxis.set_label_coords(0.0, 1.02)
    abt.add_tags(load_tags(folder))
    abt.eol_values(
        list(branches_per_obs_date.keys())[-1], values=list(data_by_cat.keys())
    )

    abt.ax.get_legend().remove()

    return abt.ax


def plot_all_ahead(
    folder: str = "./",
    date_start: str = None,
    date_end: str = None,
    exclude_patterns: list = None,
) -> plt.Axes:
    """
    Plot the worst performers in the code.
    This will primarily be used from the CLI.

    Args:
        folder (str, optionnal) : Path to the database. Defaults to "./".
        ctype (str, optionnal): Casting type, eith ahead, of behind. Defaults to True.
        date_start (str, optionnal): Starting date in "%Y-%m" format (eg.2022-04). Defaults to None.
        date_start (str, optionnal): Ending date in "%Y-%m" format (eg.2022-04). Defaults to None.
        exclude_patterns (list, optionnal): Patterns of branches to remove. Defaults to None.

    Returns:
        plt.Axes: Anubis Timegraph Axes object

    """
    branches_per_obs_date = branches_exclude_patterns(
        load_jsons(
            folder, "branch_status.json", date_start=date_start, date_end=date_end
        ),
        exclude_patterns=exclude_patterns,
    )

    # Gather all the dates for the branches.
    data_by_cat = gather_data_by_category_in_list(
        branches_per_obs_date, "branch", "ahead"
    )
    xdata_base = create_stack_plot_xbaseline(data_by_cat, "dates")

    # Merge data for branches ahead and behind with baseline.
    homogenous_db_ahead = merge_data_with_baseline(
        gather_data_by_category_in_list(branches_per_obs_date, "branch", "ahead"),
        xdata_base,
        "dates",
        "amount",
    )
    homogenous_db_behind = merge_data_with_baseline(
        gather_data_by_category_in_list(branches_per_obs_date, "branch", "behind"),
        xdata_base,
        "dates",
        "amount",
    )

    # Stack data for branches ahead and behind.
    cumulative_data_ahead = stack_data(xdata_base, homogenous_db_ahead, "amount")
    cumulative_data_behind = stack_data(xdata_base, homogenous_db_behind, "amount")

    # Extract top data points for branches ahead and behind.
    _, global_stack_ahead = cumulative_data_ahead.popitem()
    _, global_stack_behind = cumulative_data_behind.popitem()

    global_database = {
        "Unmerged contribution to commits ahead": {
            "dates": xdata_base,
            "amount": global_stack_ahead,
        },
        "Unmerged contribution to commits behind": {
            "dates": xdata_base,
            "amount": global_stack_behind,
        },
    }
    cset = tol_cset("muted")
    abt = AnubisTimeGraph("Unmerged Branches contribution to commits")
    abt.create_lineplot(
        global_database,
        "dates",
        "amount",
        cset,
        marker="o",
    )
    abt.ax.set_yscale("log")
    abt.ax.set_ylim(1, None)
    abt.ax.set_ylabel("Number of Commits", fontsize=20, rotation=0)
    abt.ax.yaxis.set_label_coords(0.0, 1.02)
    abt.add_tags(load_tags(folder))

    return abt.ax


def create_commits_activity_database(commits_per_obs_date: dict) -> dict:
    """Create commits activity database from joined database.

    Args:
        commits_per_obs_date (dict): Joined database.

    Returns:
        dict: Dictionnary of the number of commits per branch per date.
    """

    commits_activity_db = {}
    branch_names = []
    for date, commits in commits_per_obs_date.items():
        commits_activity_db[date] = {}

        # Add actives branches.
        for scom in commits:
            branches = scom["br_type"]
            for branch in branches:
                if branch not in branch_names:
                    branch_names.append(branch)
                if branch in commits_activity_db[date].keys():
                    commits_activity_db[date][branch] += 1
                else:
                    commits_activity_db[date][branch] = 1

        # Add inactives branches.
        for branch in branch_names:
            if branch not in commits_activity_db[date].keys():
                commits_activity_db[date][branch] = 0

    return commits_activity_db


def group_by_state(commits_activity_db: dict, actlim: int = 2) -> dict:
    """Group branches in two states : active/inactive.
    Branches are considerated active if the number of commits on a given date > actlim.

    Args:
        commits_activity_db (dict): Number of commits per branch per dates.
        actlim (int, optional): Activity threshold. Defaults to 2.

    Returns:
        dict: Branches classified in two categories (actives/inactives) per date.
    """

    commits_activity_db_classified = {}
    for date, branches in commits_activity_db.items():
        act = [branch for branch, nb in branches.items() if nb >= actlim]
        nb_act = len(act)
        nb_inact = len(branches) - len(act)
        commits_activity_db_classified[date.strftime("%Y-%m")] = {
            "active": nb_act,
            "inactive": nb_inact,
        }
    return commits_activity_db_classified


def formatting_db_for_histplot(
    database: dict, xkey: str = "date", catkey: str = "state"
) -> dict:
    """Format the database to match the expected format of a seaborn histogram plot.

    Args:
        database (dict): Database. {x1 : {cat1 : nb1, cat2 : nb2, ...}, x2 : {cat1 : nb1, ...}}
        xkey (str, optional): Key name of the x-axis. Defaults to 'date'.
        catkey (str, optional): Key name of the categories. Defaults to 'state'.

    Returns:
        dict: Formatted database.
    """

    stack_db = {xkey: [], catkey: []}
    for date, count in database.items():
        for cat, nb in count.items():
            for i in range(nb):
                stack_db[xkey].append(date)
                stack_db[catkey].append(cat)
    return stack_db


def plot_branch_activity_state(
    folder: str = "./",
    date_start: str = None,
    date_end: str = None,
) -> plt.Axes:
    """Plot the activity state of the branches in a repertory.
     2 states of activity are considered : active or inactive.

    Args:
        folder (str, optional): Path to the database. Defaults to ./".
        date_start (str, optional): Starting date in "%Y-%m" format (eg.2022-04). Defaults to None.
        date_end (str, optional): Ending date in "%Y-%m" format (eg.2022-04). Defaults to None.

    Returns:
        plt.Axes: Figure representing an histogramm of the branches activity state.
    """

    # Create database
    commits_per_obs_date = load_jsons(
        folder, "commits_with_br_names.json", date_start=date_start, date_end=date_end
    )
    commits_activity_db = create_commits_activity_database(commits_per_obs_date)
    commits_activity_db_grouped = group_by_state(commits_activity_db)
    plot_db = formatting_db_for_histplot(commits_activity_db_grouped)

    # Plot
    abt = AnubisTimeGraph(title=f"Branch activity state")
    abt.create_stack_histplot(
        key_for_x="date",
        key_for_data="state",
        stack_data=plot_db,
        color_list=["green", "red"],
        show_legend=True,
    )
    abt.ax.set_ylabel(f"Number of branches", fontsize=20, rotation=90)

    return abt.ax


def plot_commit_activity_by_branch(
    folder: str = "./",
    date_start: str = None,
    date_end: str = None,
) -> plt.Axes:
    """Plot the commits activity by branch in a bar chart.
    Because of the way git works, don't take into account merged and deleted branches.

    Args:
        folder (str, optional): Path to the database. Defaults to "./".
        date_start (str, optional): Starting date in "%Y-%m" format (eg.2022-04). Defaults to None.
        date_end (str, optional): Ending date in "%Y-%m" format (eg.2022-04). Defaults to None.

    Returns:
        plt.Axes: Figure representing commits activity by branch.
    """

    # Create database.
    commits_per_obs_date = load_jsons(
        folder, "commits_with_br_names.json", date_start=date_start, date_end=date_end
    )
    commits_activity_db = create_commits_activity_database(commits_per_obs_date)

    # Plot
    cmap = [
        "#2166AC",
        "#4393C3",
        "#92C5DE",
        "#D1E5F0",
        "#FDDBC7",
        "#F4A582",
        "#D6604D",
        "#B2182B",
    ]
    abt = AnubisTimeGraph(title=f"Commits activity by branch")
    abt.create_barh_plot(stack_data=commits_activity_db, cmap=cmap)
    return abt.ax


if __name__ == "__main__":
    path = "ANUBIS_OUT"
    from anubisgit.pyplot_tools import save_this_fig

    date_end = "2024-03"
    # plot_branch_activity_state(path, date_end=date_end)
    # save_this_fig("branches_activity.svg", path, width=20, height=15)
    plot_commit_activity_by_branch(path)
    save_this_fig("test.svg", path, width=20, height=15)
