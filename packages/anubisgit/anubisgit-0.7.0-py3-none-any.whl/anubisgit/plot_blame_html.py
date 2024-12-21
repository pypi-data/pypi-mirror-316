import plotly.graph_objects as go

from tol_colors import tol_cmap

from anubisgit.data_loader import load_jsons, load_authors
from anubisgit.plot_blame import gather_by_author, gather_by_age
from anubisgit.plot_common import gather_data_by_category
from anubisgit.graph_tools import stack_plot_html, get_ranges, add_tags


def plot_birth_html(
    folder: str = "./",
    date_start: str = None,
    date_end: str = None,
    by_age: bool = True,
) -> go.Figure:
    """
    Dump a raw html of the code age

    Args:
        folder (str): path to database
        date_start (str): start date of the analysis
        date_end (str): end date of the analysis
        by_age (bool): if True it's gathered by time since edition otherwise by date of last edition

    Returns:
        go.Figure: Graphical Object Figure of the birth
    """
    qoi_key = "amount"
    data_by_obs_date = gather_by_age(
        load_jsons(folder, "blame.json", date_start=date_start, date_end=date_end),
        by_age=by_age,
    )

    data_by_cat = gather_data_by_category(data_by_obs_date)

    if by_age:
        title = "Code lines gathered by time since last edition"
        cmap = tol_cmap("YlOrBr")
        largest_contributors = 0
        as_order = True
    else:
        title = "Code lines gathered by date of last edition"
        cmap = tol_cmap("WhOrBr")
        largest_contributors = 12
        as_order = True

    fig = stack_plot_html(
        data_by_cat,
        qoi_key,
        cmap=cmap,
        largest_contributors=largest_contributors,
        ascend_order=as_order,
    )

    # Update layout
    fig.update_layout(
        title_text=title,
        autosize=False,
        width=900,
        height=800,
        yaxis=dict(
            title="Lines of code",
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

    if by_age:
        fig.update_layout(legend=dict(orientation="h"), showlegend=True)

    return fig


def plot_ownership_html(
    folder: str = "./",
    date_start: str = None,
    date_end: str = None,
) -> go.Figure:
    """
    Dump a raw html with the ownership of the code lines and displaying the trigram of the author

    Args:
        folder (str): path to database
        date_start (str): start date of the analysis
        date_end (str): end date of the analysis

    Returns:
        go.Figure: Graphical Object Figure of the ownership
    """
    qoi_key = "amount"
    data_by_obs_date = gather_by_author(
        load_jsons(folder, "blame.json", date_start=date_start, date_end=date_end),
        load_authors(folder),
    )
    data_by_cat = gather_data_by_category(data_by_obs_date)
    cat_nb = len(list(data_by_cat.keys()))
    fig = stack_plot_html(
        data_by_cat,
        qoi_key,
        cmap=tol_cmap("BuRd", cat_nb),
        largest_contributors=12,
    )

    # Update layout
    fig.update_layout(
        title_text=f"Code ownership",
        autosize=False,
        width=900,
        height=800,
        yaxis=dict(
            title="Lines of code",
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
