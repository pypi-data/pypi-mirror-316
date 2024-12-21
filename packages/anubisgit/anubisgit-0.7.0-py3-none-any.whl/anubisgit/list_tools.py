"""Stupid list manipulation helpers"""


def list_reorder_by_values(names: list, values: list) -> list:
    """
    Reorder list NAMES according to VALUES

    Args:
        names (list): List of names
        values (list): List of values

    Returns:
        list : List sorted by values
    """
    return [x for _, x in sorted(zip(values, names))]


def list_running_avg(list_val: list, stencil: int) -> list:
    """
    Perform a running average on a list of float/ints

    Args:
        list_val (list): Values to average
        stencil (int): Number of values to perform average around (Crank-Nicolson way)

    Returns:
        out (list): Average list of values by weight

    """
    out = []
    for i, _ in enumerate(list_val):
        sum_ = list_val[i]
        weight = 1
        for j in range(1, stencil):
            if i - j >= 0:
                sum_ += list_val[i - j]
                weight += 1
            if i + j < len(list_val):
                sum_ += list_val[i + j]
                weight += 1
        out.append(sum_ / weight)
    return out


def list_cum_sum(list_val: list) -> list:
    """
    Perform a cumulative sum on a list of float/ints

    Args:
        list_val (list): List of values

    Returns:
        out (list): Cumulative sum of the previous values
    """
    out = [list_val[0]]
    for val in list_val[1:]:
        out.append(val + out[-1])
    return out


def list_scale(list_val: list, scale: float) -> list:
    """
    Perform a cummulative sum on a list of float/ints

    Args:
        list_val (list): List of value to scale
        scale (float): Scale factor

    Returns:
        list: List of values scaled
    """
    return [val * scale for val in list_val]
