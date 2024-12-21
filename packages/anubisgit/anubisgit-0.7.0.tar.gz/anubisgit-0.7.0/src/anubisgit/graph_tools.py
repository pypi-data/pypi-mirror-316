"""Collections of functions to help display graph"""

import datetime
from typing import Tuple

import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

from tol_colors import TOLcmaps, tol_cmap

from anubisgit.data_loader import load_tags
from anubisgit.plot_common import max_in_dicts


def get_ranges(fig: go.Figure) -> Tuple[list, list]:
    """
    Compute the boundaries for x and y axis

    Args:
        fig (obj): Plotly figure obejct

    Returns:
        x_range (list): min and max value along x axis
        y_range (list); min and max value along y axis
    """
    x_max = datetime.datetime(2000, 1, 1)
    x_min = datetime.datetime(2100, 1, 1)
    x_list = []
    for scat in fig.data:
        x_list.append(max(x_max, max(scat["x"])))
        x_list.append(min(x_min, min(scat["x"])))
    x_range = [min(x_list), max(x_list)]

    y_max = -1
    y_list = []
    for scat in fig.data:
        y_list.append(max(y_max, max(scat["y"])))
    y_range = [0, 1.1 * max(y_list)]

    return x_range, y_range


def add_tags(folder: str, x_range: list, y_range) -> Tuple[list, list]:
    """
    Add the tags to the current figure

    Args:
        folder (str): path to the database
        x_range (list): min and max value along x axis
        y_range (list): min and max value along y axis

    Returns;
        annotations_list (list): Dicts with tag names and positions
        lines_list (list): go.Scatter for tags delimitations
    """
    # Sorting tags by date
    tag_dict = {
        k: v for k, v in sorted(load_tags(folder).items(), key=lambda item: item[1])
    }
    min_x = x_range[0]
    max_x = x_range[1]
    annotations_list = []
    lines_list = []
    for tag, date in tag_dict.items():
        if date > min_x and date < max_x:
            annotations_list.append(
                {
                    "x": date,
                    "y": 0,
                    "text": tag,
                    "arrowcolor": "rgba(20, 0, 0, 0.2)",
                    "arrowside": "none",
                    "ax": 0,
                    "ayref": "y",
                    "ay": 1 * max(y_range),
                    "borderwidth": 2,
                    "bordercolor": "rgba(10, 0, 0, 0.5)",
                    "textangle": -45,
                }
            )
            y_pos = max(y_range) - 0.05

            lines_list.append(
                go.Scatter(
                    x=[date] * 10,
                    y=np.linspace(0, y_pos, 10),
                    text=f"Tag : {tag}<br>Date: {date.strftime('%Y-%m-%d')}",
                    line={"color": f"rgba(20,0,0,0.5)", "width": 2},
                    mode="lines",
                    hoverinfo="text",
                    showlegend=False,
                )
            )
    return annotations_list, lines_list


def stack_plot_html(
    data_dict: dict,
    qoi_key: str,
    cmap: TOLcmaps = None,
    largest_contributors: int = 0,
    ascend_order: bool = None,
) -> go.Figure:
    """
    Plot the html stacked plot for various data

    Args:
        data_dict (dict): Dict with various data such as dates, authors and number of commits
        qoi_key (str): Key to acces data (for exemple commits ahead or behind)
        cmap (TOLcmaps, optional): Name of the paul Tol colormap chose Defaults to None.
        largest_contributors (int, optional): Number of largest contributor. Defaults to 0.
        ascend_order (bool, optional): Bool to set to True if you wan the stack plot in ascending order. Defaults to None.

    Returns:
        go.Figure: Graph object figure of the stack plot
    """
    if cmap is None:
        cmap = tol_cmap("rainbow_WhBr").reversed()
    else:
        cmap = cmap.reversed()

    dates = []
    for cat in data_dict:
        dates.extend(data_dict[cat]["dates"])
    dates_bl = sorted(list(set(dates)))
    baseline = [0 for date in dates_bl]

    if largest_contributors > 0:
        mask_top, mask_idx = max_in_dicts(data_dict, qoi_key, largest_contributors)
    else:
        mask_top = []

    b_nb = len(list(data_dict.keys()))

    sorted_cats = list(data_dict.keys())
    if ascend_order is True:
        sorted_cats = sorted(sorted_cats)
    if ascend_order is False:
        sorted_cats = sorted(sorted_cats, reverse=True)

    fig = go.Figure()

    all_y = []
    all_names = []
    all_colors = []
    all_dates = []
    for cat_idx, cat_name in enumerate(sorted_cats):
        col_choice = round(cmap.__dict__["N"] * (cat_idx - 1) / (b_nb + 1))
        dates_b = data_dict[cat_name]["dates"]
        y_coords = data_dict[cat_name][qoi_key]

        y1_coords = []
        y2_coords = []

        for i_date, date in enumerate(dates_b):
            idx = dates_bl.index(date)
            y1_coords.append(baseline[idx])
            y2_coords.append(baseline[idx] + y_coords[i_date])
            baseline[idx] += y_coords[i_date]

        all_dates.append(dates_b)
        all_y.append(y2_coords)
        all_names.append(cat_name)
        all_colors.append(col_choice)

        if cat_idx in mask_top:
            found = mask_top.index(cat_idx)
            when = mask_idx[found]
            date = dates_b[when]
            yval = 0.5 * (y1_coords[when] + y2_coords[when])

            fig.add_annotation(
                {
                    "x": date,
                    "y": yval,
                    "text": cat_name,
                    "arrowcolor": "rgba(20, 0, 0, 0.5)",
                    "arrowside": "none",
                    "bgcolor": "rgba(255, 255, 245, 0.5)",
                    "ax": 0,
                    "ayref": "y",
                    "ay": 1.05 * yval,
                    "borderwidth": 2,
                    "bordercolor": "rgba(10, 0, 0, 0.5)",
                }
            )

    for cat_idx, y_coords in enumerate(reversed(all_y)):
        dates = list(reversed(all_dates))[cat_idx]
        name = list(reversed(all_names))[cat_idx]
        col_choice = all_colors[cat_idx]
        color = cmap(col_choice)
        rgb = f"({color[0]*255},{color[1]*255},{color[2]*255})"
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=y_coords,
                fill="tozeroy",
                fillcolor=f"rgb{rgb}",
                name=name,
                line={"color": f"rgb{rgb}", "width": 2},
                marker={"color": "rgba(0,0,0,0)"},
            )
        )
    return fig


def update_legend(fig: plt.Axes) -> plt.Axes:
    """
    Small funtion that update the legend of the current figure.

    Args:
        fig (plt.Axes): Current axes object of the figure.

    Returns:
        plt.Axes: Axes object with the legend updated.
    """
    handles, labels = fig.get_legend_handles_labels()
    legend = fig.legend(handles=handles, labels=labels)
    sns.move_legend(
        fig,
        "lower center",
        bbox_to_anchor=(0.5, -0.2),
        ncol=3,
        title=None,
        frameon=False,
        fontsize=12,
    )
    return fig
