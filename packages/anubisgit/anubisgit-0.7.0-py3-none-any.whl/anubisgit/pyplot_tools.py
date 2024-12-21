"""Some pyplot tools to help graphs display"""

import matplotlib.pyplot as plt

from loguru import logger


# TODO : REMOVE THIS FUNCTION AND PUT EVERYTHING IN GRAPH_TOOLS.PY


def add_refline(trend_coef: float, text_: str) -> None:
    """
    Add a reference line to current PYPLOT graph

    Args:
        trend_coef (float): Coefficient for line min and max scale.
        text_ (str): Text of reference line.
    """
    ax = plt.gca()
    [min_, max_] = ax.get_xlim()
    plt.plot(
        [min_, max_],
        [min_ * trend_coef, trend_coef * max_],
        color="black",
        linestyle="dotted",
    )
    plt.text(max_, trend_coef * max_, text_)


def save_this_fig(
    fname: str, anubisgit_out_dir: str, width: int = 9, height: int = 6
) -> None:
    """
    Save current maptlotlib fig

    Args:
        fname (str): File name.
        anubisgit_out_dir (_type_): Anubis output directory.
        width (int, optional): Width of plot image to save. Defaults to 9.
        height (int, optional): Height of plot image to save. Defaults to 6.
    """
    from pathlib import Path
    from matplotlib.pyplot import savefig, gcf, clf

    figure = gcf()
    figure.set_size_inches(width, height)

    fullname = Path(anubisgit_out_dir) / fname
    logger.success(f"Saving {fullname} ...")
    savefig(fullname)
    clf()
