"""Anubis pyplot reusable tools"""

from math import ceil, floor, log10
from datetime import datetime, timedelta
from typing import Union
from numpy import arange

import matplotlib.pyplot as plt
import seaborn as sns

from tol_colors import tol_cset
from loguru import logger

from matplotlib.dates import date2num
from matplotlib.ticker import FixedLocator, FixedFormatter, MultipleLocator
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm
from anubisgit.color_tools import get_color


def axis_plainticks(ax: plt.Axes, axis: str = "y"):
    """
    Switch the ticks of an axis to plain numbers and enlage to next power of ten

    The usual methods with style="csi" does not work on log scales

    Args:
        ax (plt.Axes): Matplotlib Pyplot Axes
        axis (str, optional): Name of the axis. Defaults to "y".
    """
    if axis == "x":
        min_, max_ = ax.get_xlim()
    else:
        min_, max_ = ax.get_ylim()

    floor_ = floor(log10(min_))
    ceil_ = ceil(log10(max_))

    label_list = [int(10**i) for i in range(floor_, ceil_ + 1)]
    formatter = FixedFormatter([str(i) for i in label_list])
    locator = FixedLocator(label_list)
    if axis == "x":
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.set_xlim(label_list[0], label_list[-1])
    else:
        ax.yaxis.set_major_locator(locator)
        ax.yaxis.set_major_formatter(formatter)
        ax.set_ylim(label_list[0], label_list[-1])


class AnubisTimeGraph:
    """Object to tune the typical Anubis time-deêndent graph"""

    def __init__(self, title: str = None, xlabel: str = "Date") -> None:
        """
        Baseline for time dependent plot in Anubis

        Args:
            title (str, optional): Name of the graph. Defaults to None.
            xlabel (str,optionnal): Name of the x-axis. Defaults to "Date".
        """
        self.fig, self.ax = plt.subplots()
        if title is not None:
            self.ax.set_title(title, fontsize=30, pad=30)
        self.ax.set_xlabel(xlabel, fontsize=20, labelpad=10)
        self.ax.tick_params(axis="x", labelsize=17, length=10, width=3)
        self.ax.tick_params(axis="y", labelsize=17, length=10, width=2)
        self.fig.tight_layout()
        self.change_cset()
        sns.despine()

    def change_cset(self, name="muted") -> None:
        """
        The default anubisgit color set

        Args:
            name (str, optional): Name of the Paul Tols color set. Defaults to "muted".
        """
        self.cset = tol_cset(name)

    def cset_len(self) -> int:
        """
        Number of colors in the color set

        Returns:
            int: Number of colors
        """
        return len(list(self.cset))

    def color_idx(self, idx: int) -> str:
        """
        Return color IDC from anubisgit colorset.

        Args:
            idx (int): Value of the index

        Returns:
            str: name of the color
        """
        try:
            col = list(self.cset)[idx]
        except IndexError:
            logger.warning(f"Index {idx} too large... Switching to black color")
            col = "black"
        return col

    def enlarge_right(self, factor: float = 1.2) -> None:
        """
        Enlarge x_lim right by 20% to have space for insitu labels

        Args:
            factor (float, optional): Factor to enhanced scale along x. Defaults to 1.2.
        """
        min_x, max_x = self.ax.get_xlim()
        self.ax.set_xlim(min_x, min_x + factor * (max_x - min_x))

    def enlarge_bottom(self, factor: float = 0.1) -> None:
        """
        Enlarge y_lim right by 20% to have space for tags

        Args:
            factor (float, optional): Factor to enhanced scale along y. Defaults to 0.1.
        """
        min_y, max_y = self.ax.get_ylim()
        self.ax.set_ylim(min_y - factor * (max_y - min_y), max_y)

    def add_tags(self, tag_dict: dict) -> None:
        """
        Add tags to xlabels

        Args:
            tag_dict (dict): Tags as keys and date of tags creation as items.
        """
        _, yloc = self.ax.get_ylim()
        min_x, max_x = self.ax.get_xlim()
        for tag, date in tag_dict.items():
            if date2num(date) > min_x and date2num(date) < max_x:
                self.ax.text(
                    date,
                    yloc,
                    tag,
                    ha="left",
                    va="top",
                    rotation=45,
                    bbox=dict(facecolor="white", alpha=0.8),
                )
        self.ax.set_xlabel("Date & Tags")

    def eol_values(self, x_max: Union[datetime, int], values: list = None) -> None:
        """
        Add a dotted line with the value at th end of line on the plot.
        Data needs to be from highest value to lowest along y

        Args:
            x_max (Union[datetime, int]): Max value on the x axes.
            values (list, optional): Custom values to display. Defaults to None.
        """
        last_pos = 1e9
        lower_bound = 1e9
        upper_bound = 0

        for line in self.ax.lines:
            if len(line.get_ydata()) > 0:
                lower_bound = min(lower_bound, line.get_ydata()[-1])
                upper_bound = max(upper_bound, line.get_ydata()[-1])

        threshold = (upper_bound - lower_bound) * 0.07

        pre_position = []
        for line in self.ax.lines:
            if len(line.get_xdata()) > 0:
                y_max = line.get_ydata()[-1]
                if y_max > last_pos - threshold:
                    y_max = last_pos - threshold

                pre_position.append(y_max)
                last_pos = y_max

        # # Should be the recursive part
        # for idx, position in enumerate(pre_position):
        #     if position > self.ax.get_ylim()[1] - threshold:
        #         pre_position[:idx] = [pos - threshold for pos in pre_position[:idx]]
        #     elif position < self.ax.get_ylim()[0] * 1.04:
        #         pre_position[:idx] = [pos + threshold for pos in pre_position[:idx]]

        # Creation of line to print the value in end of line
        if isinstance(x_max, datetime):
            x_line = [
                x_max + timedelta(days=10),
                x_max + timedelta(days=50),
            ]
            x_text = x_max + timedelta(days=60)

        else:
            x_line = [
                x_max + 0.3,
                x_max + 1,
            ]
            x_text = x_max + 1.2

        for idx, position in enumerate(pre_position):
            plt.plot(
                x_line,
                [
                    self.ax.lines[idx].get_ydata()[-1],
                    position,
                ],
                color=self.ax.lines[idx].get_color(),
                linestyle="--",
                linewidth=1,
                alpha=0.7,
            )

            txt = "{:.2f}".format(self.ax.lines[idx].get_ydata()[-1])
            if values:
                txt = values[idx]
            self.ax.text(
                x_text,
                position * 0.993,  # shifting for display purposes
                txt,
                fontsize=12,
                color=self.ax.lines[idx].get_color(),
            )

    def add_brackets_val(
        self, stack_data: dict, worst_candidates: dict, display_key: bool = False
    ) -> None:
        """
        Add a bracket with the value or the key to the right of the plot for the candidates in the worst_candidates dict.
        Specifically designed for stack plot or anything that involve a gap between two lines in a plot.

        Args:
            stack_data (dict): Dict with stacked values.
            worst_candidates (dict): Dict sorted by worst to best candidate.
            display_key (bool, optional): Switch to show the key instead of the value. Defaults to False.
        """

        x_ref = datetime.utcfromtimestamp(int(self.ax.lines[0].get_xdata()[-1]) * 86400)
        for idx, date_key in enumerate(stack_data.keys()):
            if date_key in worst_candidates.keys():
                y_value = self.ax.lines[idx].get_ydata()[-1]
                y_previous = [self.ax.lines[idx - 1].get_ydata()[-1] if idx > 0 else 0][
                    0
                ]
                xcoord_bracket = [
                    x_ref + timedelta(days=4),
                    x_ref + timedelta(days=8),
                    x_ref + timedelta(days=8),
                    x_ref + timedelta(days=4),
                ]
                ycoord_bracket = [
                    y_value,
                    y_value,
                    y_previous,
                    y_previous,
                ]
                plt.plot(
                    xcoord_bracket,
                    ycoord_bracket,
                    color="#000000",
                    linewidth=2,
                    linestyle="-",
                )

                to_show = worst_candidates[date_key]
                if display_key:
                    to_show = date_key
                self.ax.text(
                    x_ref + timedelta(days=20),
                    (y_previous + (y_value - y_previous) / 2) * 0.99,
                    to_show,
                    fontsize=15,
                    color="#000000",
                )

    def create_lineplot(
        self,
        data_dict: dict,
        key_for_x: str,
        key_for_y: str,
        cmap: Union[LinearSegmentedColormap, ListedColormap],
        drawstyle: str = "default",
        marker: str = "",
        specific_candidates: list = None,
    ) -> None:
        """
        Create the lineplots from database.

        Args:
            data_dict (dict): Database from which to plot.
            key_for_x (str): Name of the x_key in the database.
            key_for_y (str): Name of the y_key of the database.
            cmap (Union[LinearSegmentedColormap, ListedColormap]): Color map used for the graph.
            drawstyle (str, optional): Linestyle for the graph. Defaults to "default".
            marker (str, optional): Marker type. Defaults to "".
            specific_candidates (list, optional): Name of the specific candidates if authors are selected. Defaults to None.
        """
        color_idx = 0
        for spec_candidate in specific_candidates or data_dict:
            color = get_color(cmap, color_idx, len(data_dict))
            sns.lineplot(
                x=data_dict[spec_candidate][key_for_x],
                y=data_dict[spec_candidate][key_for_y],
                marker=marker,
                markersize=7,
                linewidth=3,
                color=color,
                label=spec_candidate,
                drawstyle=drawstyle,
                ax=self.ax,
                errorbar=None,
            )
            color_idx += 1

        handles, labels = self.ax.get_legend_handles_labels()
        legend = self.ax.legend(handles=handles, labels=labels)
        sns.move_legend(
            self.ax,
            "lower center",
            bbox_to_anchor=(0.5, -0.2),
            ncol=3,
            title=None,
            frameon=False,
            fontsize=12,
        )
        self.ax.spines[["bottom"]].set_visible(False)

    def create_stackplot(
        self,
        x_baseline: list,
        stack_data: dict,
        key_to_color: list = None,
        cmap: Union[LinearSegmentedColormap, ListedColormap] = None,
        show_legend: bool = False,
    ) -> None:
        """
        Create the stackplot given the stacked data.
        The baseline should be given and of the same length as the values

        Args:
            x_baseline (list): Span of x values.
            stack_date (dict): Dict with stacked values.
            key_to_color (list, optionnal): List of names to be colored in the graph i.e regions in the stack. Defaults to None.
            cmap (Union[LinearSegmentedColormap, ListedColormap], optionnal): Color map used for the graph. Defaults to None.
            show_legend (bool, optionnal): Display the legend from the filled areas. Defaults to False.
        """
        color_idx = 0
        previous_values = [0] * len(x_baseline)
        for data_key, values in stack_data.items():

            if key_to_color:
                if data_key in key_to_color:
                    color_idx += 1
                    color = cmap(color_idx)
                else:
                    color = (0.3, 0.3, 0.3)
            else:
                color = get_color(cmap, color_idx, len(stack_data.keys()))
                color_idx += 1

            sns.lineplot(
                x=x_baseline, y=values, color="#000000", linewidth=1, ax=self.ax
            )

            fill = self.ax.fill_between(
                x_baseline,
                previous_values,
                values,
                alpha=0.9,
                color=color,
            )

            if show_legend:
                fill.set_label(data_key)
            previous_values = values

        if show_legend:
            # Add legend with custom proxy artists
            handles, labels = self.ax.get_legend_handles_labels()
            legend = self.ax.legend(handles=handles, labels=labels)
            for handle in legend.legend_handles:
                handle.set_edgecolor("black")
            sns.move_legend(
                self.ax,
                "lower center",
                bbox_to_anchor=(0.5, -0.2),
                ncol=5,
                title=None,
                frameon=False,
                fontsize=17,
            )
        self.ax.spines[["bottom"]].set_visible(False)

    def create_stack_histplot(
        self,
        key_for_data: str,
        stack_data: dict,
        color_list: list,
        key_for_x: str = "date",
        show_legend: bool = True,
    ) -> None:
        """Create a stack histplot from database.

        Note:
            Histplot counts the number of occurences per category for a given x-axis value
            in the data.
            This means that the stack_data format must be :
            {
               'k_for_x' : [val1, val1, val1, val2, ...],
            'k_for_data' : [cat1, cat1, cat2, cat1, ...]
            }

        Args:
            k_for_data (str): Key name of the data in stack_data.
            stack_data (dict): Dict with data.
            color_list (list): Color list used to identify categories.
            k_for_x (str): Key name of the x-axis in stack_data. Defaults to 'date'.
            show_legend (bool, optional): Display the legend. Defaults to True.
        """

        # Plot
        sns.histplot(
            data=stack_data,
            x=key_for_x,
            multiple="stack",
            stat="count",
            linewidth=1,
            ax=self.ax,
            hue=key_for_data,
            palette=color_list,
            legend=show_legend,
        )

        plt.xticks(rotation=45)

        if show_legend:
            sns.move_legend(
                self.ax,
                "lower center",
                bbox_to_anchor=(0.5, -0.22),
                ncol=5,
                title=None,
                frameon=False,
                fontsize=17,
            )

        self.ax.xaxis.set_major_locator(MultipleLocator(6))

    def create_barh_plot(
        self, stack_data: dict, cmap: list, bin_range: int = 10, width: int = 31
    ) -> None:
        """Create a barh plot with data measured over time.
        Data is divided in len(cmap) bins. Each range corresponds to a color in cmap.

        Args:
            stack_data (dict): Dict with data.
            cmap (list): Discrete color map.
            bin_range (int, optional): Size of bins. Defaults to 10.
            width (int, optional): Bar's width. Defaults to 31.
        """

        # Create list of bins
        colbins = self.create_color_bins(cmap, bin_range)

        for data_key, values in stack_data.items():
            for name, nb in values.items():
                self.ax.barh(
                    y=name,
                    width=width,  # nb of days
                    left=data_key,
                    color=self.get_color_by_range(nb, colbins, cmap),
                    height=0.5,
                )

        plt.subplots_adjust(right=0.75)
        # self.ax.get_yaxis().set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_visible(False)
        self.ax.yaxis.set_label_position("right")
        self.ax.yaxis.tick_right()
        self.ax.set_xlim(right=data_key)
        self.ax.tick_params(right=False)
        self.ax.tick_params(axis="y", labelsize=13)
        norm = BoundaryNorm(colbins, len(cmap))
        cmap = ListedColormap(cmap)

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        # sm.set_array([])
        cbar = plt.colorbar(
            sm,
            ax=self.ax,
            norm=norm,
            boundaries=colbins,
            orientation="horizontal",
            aspect=40,
        )
        tick_labels = [f"{bins}" for bins in colbins]
        tick_labels[-1] += "+"
        cbar.set_ticklabels(tick_labels)
        cbar.set_label("Number of commits", size=20)

        cbar.ax.tick_params(labelsize=17)

    def create_color_bins(self, cmap: list, intrg: int = 10) -> list:
        """Create bins for each color in a discrete cmap.

        Args:
            cmap (list): List of colors.
            intrg (int, optional): Size of bins. Defaults to 10.

        Returns:
            list: List of bins.
        """
        return [i for i in range(0, intrg * (len(cmap) + 1), intrg)]

    def get_color_by_range(self, x: int, bins: list, cmap: list) -> str:
        """Return the color of the bins to which a value belongs.
        If the value >= right boundary of the list of bins, it will be considered as belonging to the last bin.

        Args:
            x (int): Value.
            bins (list): List of bins.
            cmap (list): List of colors.

        Returns:
            str: Color.
        """
        if x >= bins[-1]:
            return cmap[-1]
        for i in range(len(bins) - 1):
            if bins[i] <= x < bins[i + 1]:
                return cmap[i]
