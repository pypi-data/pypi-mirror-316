import datetime

import numpy as np
import plotly.graph_objects as go

from tol_colors import tol_cset, tol_cmap

from anubisgit.plot_branches import (
    branches_exclude_patterns,
    most_delayed_branches,
    branches_as_dicts,
)
from anubisgit.data_loader import load_jsons

from anubisgit.color_tools import hex_to_rgb
from anubisgit.graph_tools import get_ranges, add_tags, stack_plot_html

cset = tol_cset("muted")


def plot_worst_branches_html(
    folder: str = "./",
    ctype: str = "behind",
    date_start: str = None,
    date_end: str = None,
    nbranches: int = 10,
    exclude_patterns: list = None,
) -> go.Figure:
    """
    Dump a raw html with the 10 worst branches behind

    Args:
        folder(str, optionnal): Path to database. Defaults to "./".
        ctype(str, optionnal): Parameters could be score,indentation,params,cyclomatic,size. Defaults to "behind".
        date_start (str, optionnal): Start date for the analysis. Defaults to None.
        date_end (str, optionnal): End date for the analysis. Defaults to None.
        nbranches (int, optionnal); Number of branches chosen. Defaults to 10.
        exclude_patterns (list, optionnal): Patterns excluded from the complexity join dictionnary. Defaults to None.

    Returns:
        go.Figure: Graphical Object Figure of the worst branches
    """
    joined_branches = branches_exclude_patterns(
        load_jsons(
            folder, "branch_status.json", date_start=date_start, date_end=date_end
        ),
        exclude_patterns=exclude_patterns,
    )

    dict_top10 = most_delayed_branches(
        joined_branches, cat_key="branch", qoi_key=ctype, selection_size=nbranches
    )
    fig = go.Figure()

    for idx, name in enumerate(list(dict_top10.keys())[-nbranches:]):
        # Hex color to rgb color
        color = cset[idx].lstrip("#")
        color = hex_to_rgb(color)

        dates = dict_top10[name]["dates"]
        score = dict_top10[name]["score"]

        fig.add_trace(
            go.Scatter(
                x=dates,
                y=score,
                name=name,
                text=["{:,.3f}".format(score_) for score_ in score],
                line={"color": f"rgb{color}", "width": 2},
                marker={"color": f"rgb{color}", "size": 10},
                mode="lines+markers",
                hoverinfo="name+text",
            )
        )

    x_range, y_range = get_ranges(fig)

    # Update layout
    fig.update_layout(
        title_text=f"Top {nbranches} Worst performers by commits {ctype}",
        autosize=False,
        width=900,
        height=800,
        legend=dict(orientation="h"),
        dragmode="zoom",
        template="plotly_white",
        margin=dict(t=80, b=30),
        xaxis=dict(
            autorange=True,
            zeroline=True,
            type="date",
        ),
        yaxis=dict(
            title=f"{ctype}",
            zeroline=True,
            autorange=False,
            range=y_range,
        ),
    )

    # Adding tags area and names
    annotations_list, lines_list = add_tags(folder, x_range, y_range)
    for idx, annotation in enumerate(annotations_list):
        fig.add_annotation(annotation)
        fig.add_traces(lines_list[idx])

    return fig


def plot_global_branches_html(
    folder: str = "./",
    switch_behind: bool = True,
    date_start: str = None,
    date_end: str = None,
    exclude_patterns: list = None,
) -> go.Figure:
    """
    Dump a raw html with the sedimentation of branches
    ahead evolution through time

    Args:
        folder(str): path to database
        switch_behind (bool): change the qoi_key in order to look at commit behind or ahead
        date_start (str): start date for the analysis
        date_end (str): end date for the analysis
        exclude_patterns (list): str, patterns excluded from the complexity join dictionnary
    """

    cmap = tol_cmap("sunset")

    joined_branches = branches_exclude_patterns(
        load_jsons(
            folder, "branch_status.json", date_start=date_start, date_end=date_end
        ),
        exclude_patterns=exclude_patterns,
    )

    if switch_behind:
        qoi_key = "behind"

    else:
        qoi_key = "ahead"
    bdict = branches_as_dicts(joined_branches)
    fig = stack_plot_html(bdict, qoi_key, cmap, largest_contributors=6)

    # Update layout
    fig.update_layout(
        title_text=f"Worst performers by commits {qoi_key}",
        autosize=False,
        width=900,
        height=800,
        yaxis=dict(
            title=f"{qoi_key}",
            zeroline=True,
        ),
        showlegend=False,
    )

    x_range, y_range = get_ranges(fig)
    # Adding tags area and names
    annotations_list, lines_list = add_tags(folder, x_range, y_range)
    for idx, annotation in enumerate(annotations_list):
        fig.add_annotation(annotation)
        fig.add_traces(lines_list[idx])

    return fig
