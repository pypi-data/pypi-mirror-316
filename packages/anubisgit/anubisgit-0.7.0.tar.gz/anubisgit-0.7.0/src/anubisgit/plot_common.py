"""Common features for plots"""

import numpy as np
from typing import Tuple


def gather_data_by_category(
    data_by_obs_date: dict,
) -> dict:
    """
    Transpose a data by observation into a data by category

    Note:
        data_by_obs_date
            {
                -obs_date_1-: {
                    "cat1":  amount_cat1
                    "cat2":  amount_cat2
                    "cat3":  amount_cat3
                },
                -obs_date_2-: {
                    "cat1":  amount_cat1
                    "cat2":  amount_cat2
                    "cat3":  amount_cat3
                }
            }

        data_by_cat
            {
                -cat1-: {
                    "date":  list(datetime)
                    "amount":  list(int)
                },
                -cat2-: {
                    "date":  list(datetime)
                    "amount":  list(int)
                },
                -cat3-: {
                    "date":  list(datetime)
                    "amount":  list(int)
                }
            }
    Args:
        data_by_objs_date (dict): Dict of data with date as keys

    Returns:
        (dict): Dict of dat with category as keys

    """
    out = dict()

    for obs_date, data in data_by_obs_date.items():
        for category, amount in data.items():
            if category not in out:
                out[category] = {"dates": [], "amount": []}
            out[category]["dates"].append(obs_date)
            out[category]["amount"].append(amount)

    return out


def gather_data_by_category_in_list(
    data_by_obs_date: dict, key_to_focus: str, qoi_key
) -> dict:
    """
    Transpose a data by observation into a data by category targetting specific keys.
    Useful for branches data.

    Note:
        data_by_obs_date
            {
                -obs_date_1-: {
                    "cat1":  amount_cat1
                    "cat2":  amount_cat2
                    "cat3":  amount_cat3
                },
                -obs_date_2-: {
                    "cat1":  amount_cat1
                    "cat2":  amount_cat2
                    "cat3":  amount_cat3
                }
            }

        data_by_cat
            {
                amount_cat1[0]: {
                    "dates":  list(datetime)
                    "amount":  list(int)
                },
                amount_cat1[1]: {
                    "dates":  list(datetime)
                    "amount":  list(int)
                },
                amount_cat1[2]: {
                    "dates":  list(datetime)
                    "amount":  list(int)
                }
            }
    Args:
        data_by_objs_date (dict): Dict of data with date as keys
        key_to_focus (str): Category that will have its values as main key
        qoi_key (str): Key for the amounts values.


    Returns:
        (dict): Dict of dat with category as keys
    """
    out = dict()

    for obs_date, data in data_by_obs_date.items():
        for location, category in enumerate(data[key_to_focus]):
            if category not in out:
                out[category] = {"dates": [], "amount": []}
            out[category]["dates"].append(obs_date)
            out[category]["amount"].append(data[qoi_key][location])
    return out


def max_in_dicts(
    dodol: dict, key_lvl2: str, nb_contributors: int = 6
) -> Tuple[list, list]:
    """
    Find what are the biggest contributors to the sum of *key key_lvl2* and when

    Note:
        {
            contributor1: {
                "attribute1":  list()
                "attribute2":  list()
                "attribute3": list()
            },
            contributor2: {
                "attribute1":  list()
                "attribute2":  list()
                "attribute3": list()
            }
        }

        If there are less contributors (1st lvl keys) than
        nb_contributors, nb_contributors is reduced accordingly.

    Example:

        "RELEASE/0.7.3": {
            "date":  list(datetime)
            "behind":  list(int)
            "ahead": list(int)
            "nb_commits_ref_branch": list(int)
        }

    Args:
        dodol (dict of dict of lists) : A Two level dict of lists.
        key_lvl2 (str): The scnd lvl key used to find max.
        nb_contributors (int): Nb of top performers

    .
    Returns:
        mask_top (list): Top contributors, listed by index
        mask_idx (list ): Position of max for each top contributor
    """
    max_contrib = []
    when_contrib = []
    for guy in dodol:
        max_guy = max(dodol[guy][key_lvl2])
        max_contrib.append(max_guy)
        when_contrib.append(dodol[guy][key_lvl2].index(max_guy))

    max_contrib = np.array(max_contrib)
    depth = min(nb_contributors, max_contrib.size - 1)
    mask_top = list(np.argpartition(max_contrib, -depth)[-depth:])

    mask_idx = [when_contrib[idx] for idx in mask_top]

    return mask_top, mask_idx


def create_stack_plot_xbaseline(data_dict: dict, x_key: str) -> list:
    """From a given nested dict, this function will return a list with all the x_key data
    identified and putted in order.

    Args:
        data_dict (dict): 2 levels nested dict
        x_key (str): Key to look for and sort in dict

    Return:
        (list): x_key data sorted
    """
    all_xdata = []
    for cat in data_dict:
        all_xdata.extend(data_dict[cat][x_key])
    data_bl = sorted(list(set(all_xdata)))
    return data_bl


def merge_data_with_baseline(
    data_dict: dict, x_baseline: list, x_base_key: str, qoi_key: str
) -> dict:
    """
    From a lvl2 nested dict, flatten the dict and fill the missing value from the baseline
    in order to build a stacked plot.

    Args:
        data_dict (dict): 2 levels nested dict to flatten
        x_baseline (list): x values of the baseline
        x_base_key (str): Name of the x key (must be present in the data_dict)
        qoi_key (str): Name of the key for th y key (must be present in the data_dict)

    Returns:
        dict: Flatten dict with hue_key, x_base_key and qoi_key
    """
    homogenous_data_dict = {}
    for cat_key in sorted(list(data_dict.keys())):
        homogenous_data_dict[cat_key] = {qoi_key: []}
        for x_base in x_baseline:
            if x_base in data_dict[cat_key][x_base_key]:
                location = data_dict[cat_key][x_base_key].index(x_base)
                homogenous_data_dict[cat_key][qoi_key].append(
                    data_dict[cat_key][qoi_key][location]
                )
            else:
                homogenous_data_dict[cat_key][qoi_key].append(0)

    return homogenous_data_dict


def sort_by_highest_amount(
    database: dict,
    key_to_sort_by: str,
    span: str = "whole",
) -> dict:
    """
    Sort a lvl2 dict {"Entry_key1":  {"key_to_sort":[],"other_key":[]} , ... }
    depending on the key to sort by parameter values.


    Args:
        database (dict): Nested dictionnary to be sorted
        key_to_sort_by (str): Name of the key in which values have ot be sorted
        span (str): Chose between whole or last for the max computation. Defaults to "whole".

    Returns:
        (dict): flat dict with 10 worst key and values associated sorted by max to min value
    """

    worst_candidates = {}
    for date_key, date_dict in database.items():
        if span == "last":
            worst_candidates[date_key] = date_dict[key_to_sort_by][-1]
        else:
            worst_candidates[date_key] = max(date_dict[key_to_sort_by])
    worst_candidates = dict(
        sorted(
            worst_candidates.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:10]
    )

    return worst_candidates


def stack_data(x_baseline: list, database: dict, key_to_stack_by: str) -> dict:
    """
    Take the database and add to the next key and item in the dict the previous values.
    {"key_1" : [1,2,3], "key_2": [1,2,3]} -> {"key_1" : [1,2,3], "key_2": [2,4,6]}

    Args:
        x_baseline (list): Span of x values
        database (dict): nested dictionnary to be sorted
        key_to_stack_by (str): name of the key in which values have ot be sorted

    Returns:
        (dict): dict with stacked values
    """
    stacked_data = {}
    cumul_list = [0] * len(x_baseline)
    for date_key, date_dict in database.items():
        cumul_values = [
            cumul_list[idx] + value
            for idx, value in enumerate(date_dict[key_to_stack_by])
        ]
        stacked_data[date_key] = cumul_values
        cumul_list = cumul_values

    return stacked_data
