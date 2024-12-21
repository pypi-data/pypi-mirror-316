"""Module to track activity and frad on a code project"""

from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from matplotlib.colors import ListedColormap
from dateutil.parser import parse as parsedate
from tol_colors import tol_cset

from anubisgit.data_loader import load_authors, load_jsons
from anubisgit.datetime_tools import (
    datetime_to_day,
    timedelta_in_months,
    datetime_to_year,
    datetime_to_month,
)

from anubisgit.timegraph import AnubisTimeGraph
from anubisgit.list_tools import list_cum_sum, list_reorder_by_values, list_scale
from anubisgit.graph_tools import update_legend

INDIGO = "#332288"
CYAN = "#88CCEE"
TEAL = "#44AA99"
GREEN = "#771133"
OLIVE = "#999933"
SAND = "#DDCC77"
ROSE = "#CC6677"
WINE = "#882255"
PURPLE = "#AA4499"
COLOR_SCHEME = [TEAL, SAND, ROSE, WINE]

WORKED_DAYS_PER_YEAR = 253
COMMIT_DAY_PER_MONTH = 4
MAX_LINES_MONTH = 1000


def build_commitdays_authors(data_by_obs_time: dict, only_dev=True) -> dict:
    """
    Build author data in terms of commits days

    Args:
        data_by_obs_time (dict): Dict of datas gathered by date analysis
        only_dev (bool, optional): Switch to consider only the dev branch or all branches. Defaults to False.

    Returns:
        comday_data: (dict): Data of each author in terms of commits days
    """
    comday_data = {}
    for maindate, chunk in data_by_obs_time.items():
        if chunk is not None:
            list_auth = []

            chunk = sorted(chunk, key=lambda d: parsedate(d["date"]))
            for commit in chunk:
                if only_dev and commit["br_type"] == "other":
                    continue

                insert = commit.get("insertions", 0)
                delete = commit.get("deletions", 0)

                additions = min(max(insert - delete, 0), 2 * MAX_LINES_MONTH)

                if commit["author"]:
                    name = commit["author"]
                else:
                    break

                date = datetime_to_day(parsedate(commit["date"]))
                ### date=max(date,maindate) # avoid reversions __> does not work

                list_auth.append(name)
                if name not in comday_data:  # First record for this author
                    comday_data[name] = {
                        "start_date": date,
                        "last_date": date,
                        "date": [date],
                        "age": [0],
                        "commits_days": [1],
                        "insertions": [0],
                        "deletions": [0],
                        "additions": [0],
                    }
                if date == comday_data[name]["last_date"]:
                    # pass
                    comday_data[name]["insertions"][-1] += insert
                    comday_data[name]["deletions"][-1] += delete
                    comday_data[name]["additions"][-1] += additions

                else:  # if date > comday_data[name]["last_date"]
                    comday_data[name]["last_date"] = date
                    comday_data[name]["date"].append(date)
                    comday_data[name]["age"].append(
                        timedelta_in_months(date, comday_data[name]["start_date"])
                    )
                    comday_data[name]["insertions"].append(insert)
                    comday_data[name]["deletions"].append(delete)
                    comday_data[name]["additions"].append(additions)
                    comday_data[name]["commits_days"].append(1)

                    # store all dates, but commit day can be zero
    return comday_data


def build_dapm(
    data_by_obs_time: dict, trigram: dict, only_dev=True
) -> Tuple[list, list]:
    """
    Build list of distinct author per months

    Args:
        data_by_obs_time (dict): Dict of datas gathered by date analysis
        trigram (dict): Dict of name associated to their respective trigram
        only_dev (bool, optionnal): Stick to dev branch. Defaults to True.

    Returns:
        Tuple[list,list]: Time as datetime list. Number of authors per month.
    """
    time_axis = []
    authors_number = []
    for maindate, chunk in data_by_obs_time.items():
        nb_authors = np.nan
        if chunk is not None:
            list_auth = []
            chunk = sorted(chunk, key=lambda d: parsedate(d["date"]))
            for commit in chunk:
                if only_dev and commit["br_type"] == "other":
                    continue

                name = trigram.get(commit["author"].lower(), "XXX")
                list_auth.append(name)
            nb_authors = len(set(list_auth))

        time_axis.append(maindate)
        authors_number.append(nb_authors)
    return time_axis, authors_number


def build_dapy(
    data_by_obs_time: dict, trigram: dict, only_dev=True
) -> Tuple[list, list]:
    """
    Build list of distinct author per year

    Args:
        data_by_obs_time (dict): Dict of datas gathered by date analysis
        trigram (dict): Dict of name associated to their respective trigram
        only_dev (bool, optionnal): Stick to dev branch. Defaults to True.

    Returns:
        Tuple[list,list]: List of years. List of distinct authors
    """

    dapy = {}
    for maindate, chunk in data_by_obs_time.items():
        year = datetime_to_year(maindate)
        if year not in dapy:
            dapy[year] = []

        if chunk is not None:
            for commit in chunk:
                if only_dev and commit["br_type"] == "other":
                    continue
                name = trigram.get(commit["author"].lower(), "XXX")
                dapy[year].append(name)

    year_list = sorted(list(dapy.keys()))
    dapy_list = [len(set(dapy[year])) for year in year_list]
    return year_list, dapy_list


def build_activity(comday_data: dict, key_from: str) -> Tuple[list, list]:
    """
    Building activity from line addition by year as a cumulated sum

    Args:
        comday_data (dict): Data of each author in terms of commits days
        key_from (str): Key in the database to build the database from.

    Returns:
        Tuple[list, list]: List of years. List of lines addition activity by year
    """
    month_activity = {}
    for author in comday_data:
        for i, date in enumerate(comday_data[author]["date"]):
            month = datetime_to_month(date)
            if month not in month_activity:
                month_activity[month] = 0
            month_activity[month] += comday_data[author][key_from][i]

    month_list = sorted(list(month_activity.keys()))
    activity_comday = np.nancumsum([month_activity[month] for month in month_list])
    return month_list, activity_comday


def get_mvp(auth_list: list, auth_reach: list, main_commiters: int = 3) -> list:
    """
    Return a list of Maximum Value Players in AUTH_LIST,
    according to AUTH_REACH list of score.
    Output list len is MAIN_COMMITERS.

    Args:
        auth_list (list): List of authors name
        auth_reach (list): List of scores
        main_commiters (int,optionnal): Number of top commiters selectionned. Defaults to 3.

    Returns:
        list: List of the main commiters from highest to lowest.
    """
    mvp = list_reorder_by_values(auth_list, auth_reach)[-main_commiters:]
    return list(reversed(mvp))


def sort_trigrams_by_selected_authors(folder: str, authors_list: list) -> dict:
    """
    Sort trigrams from selected authors_list

    Args:
        folder (str): Folder path
        authors_list (list): Name of selected authors

    Returns:
        dict: Selected authors and trigrams
    """
    trigram_raw = load_authors(folder)
    trigram_list = []
    if "all" in authors_list:
        trigram_list = trigram_raw
    else:
        for author in authors_list:
            for author_trigram in trigram_raw.keys():
                if author.lower() in author_trigram.lower():
                    trigram_list.append(author_trigram)

    trigram = {}
    for trig in trigram_raw.keys():
        if trig in trigram_list:
            trigram[trig] = trigram_raw[trig]
    return trigram


def clean_authors_db(data_by_obs_time: dict, trigram: dict, only_dev=False) -> dict:
    """
    Remove unwanted authors from the database

    Args:
        data_by_obs_time (dict): Database generated for all authors
        trigram (dict): Selected authors and respective trigrams
        only_dev (bool, optional): Switch to consider only the dev branch or all branches. Defaults to False.

    Returns:
        dict: Reduced database to wanted authors
    """
    authors_db = build_commitdays_authors(data_by_obs_time, only_dev=only_dev)
    authors_data = authors_db.copy()

    for author in authors_db.keys():
        if author.lower() not in trigram:
            authors_data.pop(author, None)

    return authors_data


def gather_authors_by_trigram(trigram: dict) -> list:
    """
    Find groups of authors with same trigram

    Args:
        trigram (dict): Selected authors and respective trigrams

    Returns:
        list: List of lists of authors with same trigram
    """
    twins = []
    for name, trig in trigram.items():
        mini_twin = [name]
        for sec_name, sec_trig in trigram.items():
            if sec_trig == trig and name != sec_name:
                mini_twin.append(sec_name)
        mini_twin = sorted(mini_twin)
        if mini_twin not in twins and len(mini_twin) >= 1:
            twins.append(mini_twin)

        mini_twin = []
    return twins


def merge_authors_db_by_trigram(twins: list, authors_data: dict, sorting: str) -> dict:
    """
    Merge authors data with same trigram

    Args:
        twins (list): List of lists of authors with same trigram
        authors_data (dict): Reduced database to wanted authors
        sorting (str): Chose by which key to sort (either date or age)

    Returns:
        dict: Reduced database to wanted authors merge with those with same trigram
    """
    new_data = authors_data.copy()
    for names_grp in twins:
        to_merge = {}
        for name in names_grp:
            for author in authors_data.keys():
                if author.lower() == name:
                    to_merge.update({author: authors_data[author]})

        authors_merged = list(to_merge.keys())

        if not authors_merged:
            break

        sub_data = dict.fromkeys(to_merge[authors_merged[0]], [])
        for key in sub_data.keys():
            sub_list = []
            for author_m in authors_merged:
                if isinstance(authors_data[author_m][key], list):
                    sub_list.extend(authors_data[author_m][key])
                else:
                    sub_list.append(authors_data[author_m][key])
            sub_data[key] = sub_list
        sub_data["start_date"] = min(sub_data["start_date"])
        sub_data["last_date"] = max(sub_data["last_date"])

        positions = np.argsort(np.array(sub_data[sorting]))
        for key_, data in sub_data.items():
            if isinstance(data, list):
                sub_data[key_] = [sub_data[key_][pos] for pos in positions]

        chosen_one = authors_merged[0]
        new_data[chosen_one] = sub_data
        for author_m in authors_merged[1:]:
            new_data.pop(author_m)

    return new_data


def plot_global_additions(
    folder: str = "./", authors_list: list = ["all"], only_dev: bool = False
) -> plt.Axes:
    """
    Represent the global additions rate per month for the authors.

    Args:
        folder (str, optional): Location of the data. Defaults to "./".
        authors_list (list, optional): List of authors you want to consider. Defaults to ["all"].
        only_dev (bool, optional): Switch to consider only the dev branch or all branches. Defaults to False.

    Returns:
        plt.Axes: Representation of global addition rate.
    """
    data_by_obs_time = load_jsons(
        folder,
        "commits.json",
        date_start=None,
        date_end=None,
    )
    # Clean trigrams for selected authors
    trigram = sort_trigrams_by_selected_authors(folder, authors_list)

    # Clean authors db for selected authors
    authors_data = clean_authors_db(data_by_obs_time, trigram, only_dev=only_dev)
    month_activity_auth = {}
    for author, data in authors_data.items():
        month_activity_auth[author] = {
            "date": [],
            "additions": [],
            "commits": [],
            "dates": [],
        }
        previous_add = []
        previous_commits = []

        for jdx, date in enumerate(data["date"]):
            month = datetime_to_month(date)
            if month in month_activity_auth[author]["date"]:
                previous_add.append(data["additions"][jdx])
                if date not in month_activity_auth[author]["dates"]:
                    previous_commits.append(data["commits_days"][jdx])
                    month_activity_auth[author]["dates"].append(date)
            else:
                month_activity_auth[author]["dates"].append(date)
                month_activity_auth[author]["date"].append(month)
                if previous_commits:
                    month_activity_auth[author]["additions"].append(sum(previous_add))
                    month_activity_auth[author]["commits"].append(sum(previous_commits))
                else:
                    month_activity_auth[author]["additions"].append(
                        data["additions"][jdx]
                    )
                    month_activity_auth[author]["commits"].append(
                        data["commits_days"][jdx]
                    )

                previous_add = []
                previous_commits = []

    if previous_add or previous_commits:
        month_activity_auth[author]["additions"].append(sum(previous_add))
        month_activity_auth[author]["commits"].append(sum(previous_commits))

    gaddition_dict = {"authors": [], "additions": [], "commits": []}
    for author, data in month_activity_auth.items():
        auth = [author] * len(data["additions"])
        gaddition_dict["authors"].extend(auth)
        gaddition_dict["additions"].extend(data["additions"])
        gaddition_dict["commits"].extend(data["commits"])

    abt = AnubisTimeGraph(title="Global Addition Rate", xlabel="Commits Day")
    abt.ax.set_ylabel("Additions", fontsize=20, labelpad=10)

    scatter = sns.regplot(
        data=gaddition_dict,
        x=gaddition_dict["commits"],
        y=gaddition_dict["additions"],
        ax=abt.ax,
        order=1,
        scatter_kws={"color": "#000000", "alpha": 0.5},
        line_kws={"color": "#CC3311"},
        label=["commits", "additions"],
    )

    return abt.ax


def process_author_data(
    authors_name: list, database: dict, time_key: str, data_key: str
) -> dict:
    """
    Generate the cumulated database for authors.

    Args:
        authors_name (list): Name of the authors.
        database (dict): Database of the authors merged with similar trigrams.
        time_key (str): Chose among "date", "age" or "time".
        data_key (str): Value from which you want to plot, can be "additions". Has to be a key of the dictionnary.

    Returns:
        dict: Cumulated database for authors.
    """
    authors_processed = {}
    for author in authors_name:
        sorted_data = sorted(
            zip(database[author][time_key], database[author][data_key])
        )
        sorted_dates, sorted_additions = zip(*sorted_data)
        authors_processed[author] = {
            time_key: sorted_dates,
            data_key: list_cum_sum(sorted_additions),
        }
    return authors_processed


def process_author_data_and_mvp(
    time_key: str, data_key: str, folder: str = "./", authors_list: list = ["all"]
) -> Tuple[dict, dict]:
    """
    Create two databases for the mvp and non mvp authors.

    Args:
        time_key (str): Chose among "date", "age" or "time".
        data_key (str): Value from which you want to plot, can be "additions". Has to be a key of the dictionnary.
        folder (str, optional): Location of the data. Defaults to "./".
        authors_list (list, optional): List of authors you want to consider. Defaults to ["all"].

    Returns:
        Union[dict, dict]: Databases for mvp and non mvp authors.
    """
    # Load data
    data_by_obs_time = load_jsons(
        folder,
        "commits.json",
    )

    trigram = sort_trigrams_by_selected_authors(folder, authors_list)

    # Clean authors db for selected authors
    authors_data = clean_authors_db(data_by_obs_time, trigram)

    # Find authors with same trigram
    twins = gather_authors_by_trigram(trigram)

    # Merge authors_db to avoid evil twin
    reduced_authors_data_date = merge_authors_db_by_trigram(
        twins, authors_data, time_key
    )
    auth_list = list(reduced_authors_data_date.keys())

    mvp = get_mvp(
        auth_list,
        [
            list_cum_sum(reduced_authors_data_date[auth][data_key])[-1]
            for auth in auth_list
        ],
    )

    no_mvps = [key for key in reduced_authors_data_date if key not in mvp]
    mvps = [key for key in mvp if key in reduced_authors_data_date]

    # Process data for authors with and without MVP status
    authors_nomvp = process_author_data(
        no_mvps, reduced_authors_data_date, time_key, data_key
    )
    authors_mvp = process_author_data(
        mvps, reduced_authors_data_date, time_key, data_key
    )

    return authors_nomvp, authors_mvp


def plot_activity_cumulated(
    time_key: str,
    data_key: str,
    title: str,
    ylabel: str,
    folder: str = "./",
    xlabel: str = "Date",
    authors_list: list = ["all"],
) -> plt.Axes:
    """
    Plot cumulated values with top 3 users highlighted

    Args:
        time_key (str): Chose among "date", "age" or "time".
        data_key (str): Value from which you want to plot, can be "additions". Has to be a key of the dictionnary.
        title (str): Title of the graph.
        ylabel (str): Title of the y-axis.
        folder (str, optional): Location of the data. Defaults to "./".
        xlabel (str, optional): Title of the x-axis. Defaults to "Date".
        authors_list (list, optional): List of authors you wan to consider. Defaults to ["all"].

    Returns:
        plt.Axes: Cumulated values with top 3 highlighted.
    """
    authors_nomvp, authors_mvp = process_author_data_and_mvp(
        time_key, data_key, folder=folder, authors_list=authors_list
    )
    grey_cset = ListedColormap("lightgrey")
    cset = tol_cset("bright")
    abt = AnubisTimeGraph(title=title, xlabel=xlabel)
    abt.ax.set_ylabel(ylabel, fontsize=20, labelpad=10)
    abt.create_lineplot(authors_mvp, time_key, data_key, cset)
    abt.eol_values(
        sorted(authors_mvp[list(authors_mvp.keys())[0]][time_key])[-1],
        values=list(authors_mvp.keys()),
    )
    abt.create_lineplot(authors_nomvp, time_key, data_key, grey_cset)

    abt.ax.get_legend().remove()
    sns.despine()

    return abt.ax


def gather_authors_activity(
    folder: str = "./", authors_list: list = ["all"], only_dev: bool = True
) -> dict:
    """
    Create the database for the authors activity.

    Args:
        folder (str, optional): Location of the data. Defaults to "./".
        authors_list (list, optional): List of authors you wan to consider. Defaults to ["all"].
        only_dev (bool, optional): Switch to consider only the dev branch or all branches. Defaults to True.

    Returns:
        dict: Database of authors activity.
    """

    data_by_obs_time = load_jsons(
        folder,
        "commits.json",
        date_start=None,
        date_end=None,
    )
    # Clean trigrams for selected authors
    trigram = sort_trigrams_by_selected_authors(folder, authors_list)

    # Evaluating distinct authour presence
    year_list, dapy_list = build_dapy(data_by_obs_time, trigram, only_dev=only_dev)
    time_axis, authors_list = build_dapm(data_by_obs_time, trigram, only_dev=only_dev)

    custom_key = "On all branches"
    if only_dev:
        custom_key = "On Dev branch"

    dict_activity = {
        f"{custom_key}, per year": {"time": year_list, "auth": dapy_list},
        f"{custom_key}, per month": {"time": time_axis, "auth": authors_list},
    }
    return dict_activity


def plot_activity_authors(
    time_key: str,
    data_key: str,
    ylabel: str,
    folder: str = "./",
    authors_list: list = ["all"],
) -> plt.Axes:
    """
    Step plot representing the activity representing the number of distincts authors on dev branch and all branches.

    Args:
        time_key (str): Chose among "date", "age" or "time".
        data_key (str): Value from which you want to plot, can be "additions". Has to be a key of the dictionnary.
        ylabel (str): Title of the y-axis.
        folder (str, optional): Location of the data. Defaults to "./".
        authors_list (list, optional): List of authors you wan to consider. Defaults to ["all"].

    Returns:
        plt.Axes: Figure representing the activity on branches.
    """

    activity_dict = gather_authors_activity(folder=folder, authors_list=authors_list)
    activity_dict_all = gather_authors_activity(
        folder=folder, authors_list=authors_list, only_dev=False
    )
    cset = tol_cset("vibrant")
    abt = AnubisTimeGraph(title="Authors activity", xlabel="Date")
    abt.ax.set_ylabel(ylabel, fontsize=20, labelpad=10)
    abt.create_lineplot(
        activity_dict, time_key, data_key, cset, drawstyle="steps-post", marker=""
    )
    abt.create_lineplot(
        activity_dict_all, time_key, data_key, cset, drawstyle="steps-post", marker=""
    )
    abt.ax.lines[2].set_linestyle("dotted")
    abt.ax.lines[3].set_linestyle("dotted")
    abt.ax = update_legend(abt.ax)
    sns.despine()

    return abt.ax


def create_commits_evolution_database(data_by_obs_time: dict) -> dict:
    """Create a database for the commit activity plot.

    Args:
        data_by_obs_time (dict): Commits data.

    Returns:
        dict: Commits evolution database on the dev branch.
    """

    dict_commit_evolution = {}

    for date, commits in data_by_obs_time.items():
        list_commits = [
            scom["br_type"] for scom in commits if scom["br_type"] != "other"
        ]
        nb_commits = len(list_commits)
        if nb_commits != 0 and dict_commit_evolution == {}:  # Init
            branch_name = list_commits[0]
            dict_commit_evolution[branch_name] = {"dates": [], "commits": []}
        dict_commit_evolution[branch_name]["dates"].append(date)
        dict_commit_evolution[branch_name]["commits"].append(nb_commits)

    return dict_commit_evolution


def plot_commit_activity(folder: str = "./") -> plt.Axes:
    """Plot of the number of commits along time for a branch. Doesn't show the authors.

    Args:
        folder (str, optional): Location of the data. Defaults to "./".

    Returns:
        plt.Axes: Figure representing the commit activity on the dev branch.
    """

    data_by_obs_time = load_jsons(folder, "commits.json")

    db = create_commits_evolution_database(data_by_obs_time)
    branch_name = list(db.keys())[0]

    cset = tol_cset("muted")
    abt = AnubisTimeGraph(title=f"Commit activity on {branch_name}", xlabel="Date")
    abt.ax.set_ylabel("Number of Commits", fontsize=20, labelpad=10)
    abt.create_lineplot(db, "dates", "commits", cset)
    sns.despine()

    return abt.ax
