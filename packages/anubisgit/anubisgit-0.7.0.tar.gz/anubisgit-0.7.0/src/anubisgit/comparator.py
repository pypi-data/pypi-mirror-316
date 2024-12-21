"""Helps anubisgit to handle names and remove same user with different names as well
as building aliases for them.

Adapted from https://github.com/dchaplinsky/comparator due to inactivity of the
developer.
"""

import re
from typing import Callable, Union
from functools import reduce
from itertools import permutations, islice, zip_longest
from operator import mul
from Levenshtein import jaro, jaro_winkler


def _smart_jaro(a: list, b: list, func: Callable = jaro) -> Union[bool, float]:
    """
    Used to compute the distance between 2 names

    Args:
        a (list): letters of first name
        b (list): letters of second name
        func (Callable, optional): Function used to compare the lists. Defaults to jaro.

    Returns:
        Union[bool, float]: True if it's the same character, otherwise it runs the chunk_distance.
    """
    if func(a[1:], b[1:]) > 0.99:
        return True

    if func(a, b[1:]) > 0.99:
        return True

    if func(a[1:], b) > 0.99:
        return True

    chunk_distance = max([func(a, b)])
    if abs(len(a) - len(b)) >= 3:
        chunk_distance -= 0.2

    return chunk_distance


def _compare_two_names(
    name1: str, name2: str, straight_limit: float = 0.70, smart_limit: float = 0.96
) -> bool:
    """
    Compares two names to see if they may be the same.

    Args:
        name1 (str): first name
        name2 (str): seconde name
        straight_limit (float, optional): Arbitrary limit for similarity. Defaults to 0.70.
        smart_limit (float, optional): Limit set to avoid doing other computation to compare. Defaults to 0.96.

    Returns:
        bool: True if names are similars.
    """
    straight_similarity = jaro(name1, name2)
    if straight_similarity > smart_limit:
        return True

    if straight_similarity > straight_limit:
        min_pair_distance = 1
        for a, b in zip_longest(name1.split(" "), name2.split(" ")):
            if a is not None and b is not None:
                chunk_distance = _smart_jaro(a, b, func=jaro_winkler)
                min_pair_distance = min(chunk_distance, min_pair_distance)

        if min_pair_distance > 0.88:
            return True

    return False


def _normalize_name(s: str) -> str:
    """
    Small function replacing unwanted characters.

    Args:
        s (str): name

    Returns:
        str: normalized name
    """
    return (
        re.sub(r"\s+", " ", s.strip().replace("-", " "))
        .replace(".", "")
        .replace(",", "")
        .replace('"', "")
        .replace("'", "")
        .replace("’", "")
        .replace("є", "е")
        .replace("i", "и")
        .replace("і", "и")
        .replace("ь", "")
        .replace("'", "")
        .replace('"', "")
        .replace("`", "")
        .replace("конст", "кост")
        .replace("’", "")
        .replace("ʼ", "")
    )


def _slugify_name(s: str) -> str:
    """
    Remove unwanted spacing in names

    Args:
        s (str): name

    Returns:
        str: name without spaces
    """

    s = s.replace(" ", "")

    return re.sub(r"\d+", "", s)


def _thorough_compare(name1: str, name2: str, max_splits: int = 7) -> bool:
    """
    Compare two names

    Args:
        name1 (str): First name to compare
        name2 (str): Second name to compare
        max_splits (int, optional): Number of maximum splits. Defaults to 7.

    Returns:
        bool: True if they're the same
    """
    splits = name2.split(" ")
    limit = reduce(mul, range(1, max_splits + 1))

    for opt in islice(permutations(splits), limit):
        if _compare_two_names(name1, " ".join(opt)):
            return True

    return False


def full_compare(name1: str, name2: str) -> bool:
    """
    Full comparison of two names/

    Args:
        name1 (str): First name to compare
        name2 (str): Second name to compare

    Returns:
        bool: True if they're the same
    """
    name1 = _normalize_name(name1)
    name2 = _normalize_name(name2)
    slugified_name1 = _slugify_name(name1)
    slugified_name2 = _slugify_name(name2)

    if slugified_name1 == slugified_name2:
        return True

    if slugified_name1.startswith(slugified_name2) and len(slugified_name2) >= 10:
        return True

    if slugified_name2.startswith(slugified_name1) and len(slugified_name1) >= 10:
        return True

    if slugified_name1.endswith(slugified_name2) and len(slugified_name2) >= 10:
        return True

    if slugified_name2.endswith(slugified_name1) and len(slugified_name1) >= 10:
        return True

    if jaro(slugified_name1, slugified_name2) > 0.95:
        return True

    # Function is symetric, no need
    # if jaro(slugified_name2, slugified_name1) > 0.95:
    #     return True

    if _compare_two_names(name1, name2):
        return True

    # Function is symetric, no need
    # if _compare_two_names(name2, name1):
    #     return True

    return _thorough_compare(name1, name2) or _thorough_compare(name2, name1)
