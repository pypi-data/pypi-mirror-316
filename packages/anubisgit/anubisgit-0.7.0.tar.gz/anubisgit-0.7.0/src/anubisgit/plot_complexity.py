""" File that gathers complexity plot only"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from math import log
from datetime import datetime

from tol_colors import tol_cset

from anubisgit.data_loader import load_jsons, load_tags
from anubisgit.timegraph import AnubisTimeGraph
from tucan.struct_common import complexity_score

GLOBAL_COMPLEXITY_METRICS = {
    "score": "score",
    "CCN": "cyclomatic",
    "IDT_int": "indentation",
    "HDF": "halstead_diff",
    "NLOC": "size",
}


def complexity_worst_performers(
    joined_complexity: dict, nfunc: int = 10, ctype: str = "score"
) -> dict:
    """
    Identify worst performers in complexity

    Args:
        joined_complexity (dict): Complexity data acquired from the .json joined db.
        nfunc (int, optional): Number of worst performers to keep. Defaults to 10.
        ctype (str, optional): Complexity metrics to target for ranking. Defaults to "score".

    Returns:
        dict: Top 10 dict stored by name
    """

    dict_top10 = {}
    for date, dataset in joined_complexity.items():
        cplx_score = complexity_score(dataset)
        cc_com = cplx_score[ctype]
        cc_files = dataset["file"]
        cc_functions = dataset["function"]

        local_max = min(nfunc, cc_com.size - 1)
        mask_top10 = np.argpartition(cc_com, -local_max)[-local_max:]
        for index in mask_top10:
            name = f"{cc_files[index]}/\n{cc_functions[index]}"
            if name not in dict_top10:
                dict_top10[name] = {
                    "dates": [],
                    "score": [],
                }
            dict_top10[name]["dates"].append(date)
            dict_top10[name]["score"].append(cc_com[index])

    for name in dict_top10:
        dict_top10[name]["score"] = np.array(dict_top10[name]["score"])
    return dict_top10


def _create_complexity_plot_database(
    joined_complexity: dict, ctype: str = "global"
) -> dict:
    """
    Function that handles the creation and organization of the database for the
    complexity plot.
    Complexities are ponderated by NLOC

    Args:
        joined_complexity (dict): Complexity data acquired from the .json joined db
        ctype (str) : Complexity metric to plot. Default to "global".

    Returns:
        (dict): dict with each complexity with their dates and values
    """

    # Gather only the last to date value of the complexity to arrange in croissant order
    if ctype == "global":
        complexity_dict = {
            metric: {"dates": [], "values": []}
            for metric in GLOBAL_COMPLEXITY_METRICS.values()
        }
    else:
        complexity_dict = {
            GLOBAL_COMPLEXITY_METRICS[ctype]: {"dates": [], "values": []}
        }

    for date, dict_ in joined_complexity.items():
        if ctype == "global":
            cplx_score = complexity_score(dict_)
        else:
            cplx_score = {
                GLOBAL_COMPLEXITY_METRICS[ctype]: np.array(
                    dict_[ctype], dtype=np.float64
                )
            }

        for complexity_name in complexity_dict.keys():
            complexity_val = cplx_score[complexity_name]
            nloc = dict_["NLOC"]
            complexity_dict[complexity_name]["values"].append(
                np.sum(complexity_val * nloc) / np.sum(nloc)
            )
            complexity_dict[complexity_name]["dates"].append(date)

    return complexity_dict


def create_worst_performers_database(dict_top10: dict, n_element: int) -> dict:
    """
    Function that handles the creation and organization of the database for the
    worts performers complexity plot. Aim to fully exploit seaborn lineplot.

    Args:
        dict_top10 (dict): Top 10 dict stored by name
        n_element (int): Number of worst performers to keep.

    Returns:
        (dict): Flat dict ordered by key with the lowest values to the highest
    """

    # Ordering the previous dict
    contestants = {}
    for file in dict_top10.keys():
        contestants[file] = dict_top10[file]["score"][-1]
    contestants = dict(sorted(contestants.items(), key=lambda item: item[1]))

    # iteration in reverse, so If we end up with too many performers,
    # the olders are skipped
    dict_worst_performers = {}
    for idx, name in enumerate(reversed(list(contestants.keys()))):
        if idx > n_element - 1:
            break
        dict_worst_performers[name] = {"dates": [], "score": []}
        dict_worst_performers[name]["dates"].extend(dict_top10[name]["dates"])
        dict_worst_performers[name]["score"].extend(dict_top10[name]["score"])

    return dict_worst_performers


def plot_complexity(
    folder: str = "./",
    ctype: str = "global",
    date_start: str = None,
    date_end: str = None,
) -> plt.Axes:
    """
    The plots of complexity along time

    Args:
        folder (str, optional): Path to the source folder. Defaults to "./".
        ctype (str, optional): Complexity metrics to target for ranking. Defaults to "score".
        date_start (str, optional): Date start included, using strptime format %Y-%m-%d. Defaults to None.
        date_end (str, optional): Date end included, using strptime format %Y-%m-%d. Defaults to None.

    Returns:
        plt.Axes: Anubis Timegraph Axes object
    """

    joined_complexity = load_jsons(
        folder, "complexity.json", date_start=date_start, date_end=date_end
    )
    complexity_dict = _create_complexity_plot_database(joined_complexity, ctype)
    sorted_complexity_dict = {
        k: v
        for k, v in sorted(
            complexity_dict.items(),
            key=lambda item: item[1]["values"][-1],
            reverse=True,
        )
    }

    if ctype == "global":
        abt = AnubisTimeGraph(title="Global Complexity")
        abt.ax.set_ylabel("Score - 0 (good) to 10 (bad)", fontsize=20, labelpad=10)
    else:
        abt = AnubisTimeGraph(
            title=f"{GLOBAL_COMPLEXITY_METRICS[ctype].capitalize()} Complexity"
        )
        abt.ax.set_ylabel(
            f"{GLOBAL_COMPLEXITY_METRICS[ctype].capitalize()}", fontsize=20, labelpad=10
        )
    cset = tol_cset("muted")
    abt.create_lineplot(sorted_complexity_dict, "dates", "values", cset)

    if ctype == "global":  # normalized
        abt.ax.set_ylim(0, 10)

    # Ensure that the EOL are well located
    x_max = datetime(1800, 1, 1)
    for main_key in sorted_complexity_dict.keys():
        x_max = max(x_max, sorted_complexity_dict[main_key]["dates"][-1])

    abt.eol_values(x_max)
    abt.ax.legend()
    sns.move_legend(
        abt.ax,
        "upper center",
        bbox_to_anchor=(0.5, 1.05),
        ncol=5,
        title=None,
        frameon=False,
        fontsize=17,
    )
    abt.add_tags(load_tags(folder))
    sns.despine()

    return abt.ax


def plot_worst_performers(
    folder: str = "./",
    ctype: str = "score",
    date_start: str = None,
    date_end: str = None,
    nfunc: int = 10,
) -> plt.Axes:
    """
    Plot the worst performers in the code

    Args:
        folder (str, optional): Path to the source folder. Defaults to "./".
        ctype (str, optional): Complexity metrics to target for ranking. Defaults to "score".
        date_start (str, optional): Date start included, using strptime format %Y-%m-%d. Defaults to None.
        date_end (str, optional): Date end included, using strptime format %Y-%m-%d. Defaults to None.
        nfunc (int, optional): Number of worst performers to keep. Defaults to 10.

    Returns:
        plt.Axes: Anubis Timegraph Axes object
    """
    joined_complexity = load_jsons(
        folder, "complexity.json", date_start=date_start, date_end=date_end
    )

    dict_top10 = complexity_worst_performers(
        joined_complexity,
        nfunc=nfunc,
    )

    dict_worst_performers = create_worst_performers_database(dict_top10, nfunc)
    cset = tol_cset("muted")

    abt = AnubisTimeGraph(title="Worst performers")
    abt.ax.set_ylabel(
        f"{ctype.capitalize()} - 0 (good) to 10 (bad)", fontsize=20, labelpad=10
    )
    abt.create_lineplot(dict_worst_performers, "dates", "score", cset)

    abt.ax.set_ylim(0, 10)

    # Ensure that the EOL are well located
    x_max = datetime(1800, 1, 1)
    for main_key in dict_worst_performers.keys():
        x_max = max(x_max, dict_worst_performers[main_key]["dates"][-1])
    abt.eol_values(x_max)

    abt.add_tags(load_tags(folder))
    abt.ax.legend()
    sns.move_legend(
        abt.ax,
        "lower center",
        bbox_to_anchor=(0.5, -0.3),
        ncol=3,
        title=None,
        frameon=False,
        fontsize=12,
    )
    sns.despine()

    return abt.ax
