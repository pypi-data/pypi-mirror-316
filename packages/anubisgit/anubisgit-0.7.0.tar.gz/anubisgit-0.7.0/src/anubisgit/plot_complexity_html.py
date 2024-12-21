import os
import datetime

import numpy as np
import plotly.graph_objects as go

from tol_colors import tol_cset

from anubisgit.plot_complexity import (
    complexity_worst_performers,
    complexity_score,
)
from anubisgit.data_loader import load_jsons
from anubisgit.color_tools import hex_to_rgb
from anubisgit.graph_tools import get_ranges, add_tags

cset = tol_cset("muted")


def plot_worst_performers_html(
    folder: str = "./",
    date_start: str = None,
    date_end: str = None,
) -> go.Figure:
    """
    Create a plotly html Figure with the 10 worst performers

    Args:
        folder(str, optionnal): Path to database. Defaults to "./".
        date_start (str, optionnal): start date for the analysis. Defaults to None.
        date_end (str, optionnal): end date for the analysis. Defaults to None.

    Returns:
        go.Figure: Graphical Object Figure of the worst branches
    """
    joined_complexity = load_jsons(
        folder, "complexity.json", date_start=date_start, date_end=date_end
    )
    dict_top10 = complexity_worst_performers(joined_complexity)

    fig = go.Figure()

    # iteration in reverse, so If we end up with too many performers,
    # the olders are skipped
    # for idx, name in enumerate(dict_top10.keys()):
    for idx, name in enumerate(list(dict_top10.keys())[-10:]):

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
        title_text="Worst performers",
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
            title="Score - 0 (good) to 10 (bad)",
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


def plot_global_complexity_html(
    folder: str = "./",
    ctype: str = "score",
    date_start: str = None,
    date_end: str = None,
) -> go.Figure:
    """
    Create a plotly html Figure of the global complexity for score, indentation, params, cyclomatic and size.

    Args:
        folder(str, optionnal): Path to database. Defaults to "./".
        ctype(str, optionnal): Parameters could be score,indentation,params,cyclomatic,size. Defaults to "score".
        date_start (str, optionnal): Start date for the analysis. Defaults to None.
        date_end (str, optionnal): End date for the analysis. Defaults to None.

    Returns:
        go.Figure: Graphical Object Figure of the worst branches
    """
    joined_complexity = load_jsons(
        folder, "complexity.json", date_start=date_start, date_end=date_end
    )
    ldates = []
    data_complexity = {
        "Score": [],
        "Indentation": [],
        "Cyclomatic": [],
        # "Params": [],
        "Size": [],
    }
    for date, dict_ in joined_complexity.items():
        cplx_score = complexity_score(dict_)
        nloc = dict_["NLOC"]
        ldates.append(date)
        data_complexity["Score"].append(
            np.sum(cplx_score["score"] * nloc) / np.sum(nloc)
        )
        data_complexity["Indentation"].append(
            np.sum(cplx_score["indentation"] * nloc) / np.sum(nloc)
        )
        data_complexity["Cyclomatic"].append(
            np.sum(cplx_score["cyclomatic"] * nloc) / np.sum(nloc)
        )
        # data_complexity["Params"].append(np.sum(dict_["params"] * nloc) / np.sum(nloc))
        data_complexity["Size"].append(np.sum(cplx_score["size"] * nloc) / np.sum(nloc))

    # Create figure
    fig = go.Figure()
    for idx, ctype in enumerate(data_complexity):
        # Hex color to rgb color
        color = cset[idx].lstrip("#")
        color = hex_to_rgb(color)

        fig.add_trace(
            go.Scatter(
                x=ldates,
                y=data_complexity[ctype],
                name=ctype,
                text=["{:,.3f}".format(value) for value in data_complexity[ctype]],
                hoverinfo="name+x+text",
                line={"color": f"rgb{color}", "width": 2},
                marker={"color": f"rgb{color}", "size": 6},
                mode="lines+markers",
                showlegend=True,
            )
        )

    x_range, y_range = get_ranges(fig)

    # Add range slider and update axis
    fig.update_layout(
        title_text="Global Complexity",
        dragmode="zoom",
        hovermode="x",
        template="plotly_white",
        margin=dict(t=80, b=30),
        autosize=False,
        width=1000,
        height=800,
        xaxis=dict(
            autorange=True,
            zeroline=True,
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        ),
        yaxis=dict(
            title="Score - 0 (good) to 10 (bad)",
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
