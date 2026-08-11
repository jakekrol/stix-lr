#!/usr/bin/env python3
import argparse

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pearsonr


def str_or_tuple(value):
    """
    Parse function for color-scale which should accept either a string or a tuple
    denoting the vmin and vmax values for the color scale.
    """
    match value.split(","):
        case [x, y] if x.isdigit() and y.isdigit():
            return (float(x), float(y))
        case ["log"]:
            return value
        case _:
            raise ValueError(f"Invalid color scale value: {value}")


def parse_args():
    parser = argparse.ArgumentParser(description="Plot population frequency")
    parser.add_argument("--stix", help="STIX aggregated queries bed", required=True)

    parser.add_argument("--stix_max", default=None, type=int, help="Max value for STIX")


    parser.add_argument("--other", help="Pop freq comparison bed", required=True)
    parser.add_argument("--color", default="Reds")
    parser.add_argument("--xlabel", default="Other pop freq")
    parser.add_argument("--ylabel", default="STIX 1kg 2504 SR pop freq")
    parser.add_argument("--color-scale", type=str_or_tuple, default="log",\
                        help="\"log\" or comma separated pair of numbers denoting vmin and vmax")
    parser.add_argument("--output", required=True, help="Output png file")
    parser.add_argument("--merged", required=True, help="Output merged bed file")
    parser.add_argument('--height', type=int, help="The height of the histogram", default=4)
    parser.add_argument('--width', type=int, help="The width of the histogram", default=4)
    parser.add_argument('--title', type=str, help="Plot title")

    parser.add_argument("--tick_line_length",
                        type=float,
                        default=2,
                        help="Tick line width")

    parser.add_argument("--tick_line_width",
                        type=float,
                        default=0.5,
                        help="Tick line width")

    parser.add_argument("--axis_line_width",
                        type=float,
                        default=0.5,
                        help="Axis line width")

    parser.add_argument("--axis_label_size",
                        type=int,
                        default=8,
                        help="Axis label font size")

    parser.add_argument("--tick_label_size",
                        type=int,
                        default=8,
                        help="Axis tick label font size")
    parser.add_argument("--fignum", type=str, help="Figure number")



    return parser.parse_args()


def plot_data(
    stix: str,
    other: str,
    xlabel: str,
    ylabel: str,
    color: str,
    color_scale: str | tuple[float, float],
    output: str,
    width: int,
    height: int,
    axis_label_size: int,
    tick_label_size: int,
    tick_line_length: float,
    tick_line_width: float,
    axis_line_width: float,
    title: str = None,
    stix_max: int = None,
    fignum: str = None,
    merged: str = None
):
    #label_font_size = 10
    #figwidth = 5
    #figheight = 4
    # legend_item_font_size = 8
    # legend_title_font_szie = 9
    #ticks_font_size = 12
    if color == "Reds":
        cmap = mcolors.LinearSegmentedColormap.from_list(
            "LightReds",
            ["#FFFFFF", "#FEE0D2", "#FCBBA1", "#FC9272", "#FB6A4A", "#EF3B2C", "#CB181D"],
        )
    elif color == "Blues":
        cmap = mcolors.LinearSegmentedColormap.from_list(
            "LightBlues",
            ['#FFFFFF', '#EFF3FF', '#C6DBEF', '#9ECAE1', '#6BAED6', '#4292C6', '#2171B5'],
        )
    elif color == "Greens":
        cmap = mcolors.LinearSegmentedColormap.from_list(
            "LightGreens",
            ['#FFFFFF', '#E5F5E0', '#C7E9C0', '#A1D99B', '#74C476', '#41AB5D', '#238B45'],
        )
    else:
        raise ValueError(f"Invalid color scale: {color}")

    stix_df = pd.read_csv(
        stix,
        sep="\t",
    )
    stix_df.columns = ["svid", "stix_count"]
    stix_df["stix_population_frequency"] = stix_df["stix_count"] / stix_max if stix_max else stix_df["stix_count"]
    # if stix_max:
    #     stix_df = stix_df[stix_df["stix_count"] <= stix_max]

    # for AFs that are -1 (ie missing), we will set them to 0
    other_df = pd.read_csv(
        other,
        sep="\t",
    )
    other_df.columns = ["svid", "other_population_frequency"]
    other_df["other_population_frequency"] = other_df["other_population_frequency"].apply(lambda x: 0 if x == -1 else x)

    merged_df = pd.merge(stix_df, other_df, on=["svid"])

    if merged:
        merged_df.to_csv(merged, sep="\t", index=False, header=False)

    fig, ax = plt.subplots(figsize=(width, height))
    #plt.subplots_adjust(hspace=0.0)

    f = plt.hexbin(
        x=merged_df["other_population_frequency"],
        y=merged_df["stix_population_frequency"],
        bins="log" if color_scale == "log" else None,
        vmin=color_scale[0] if type(color_scale) == tuple else None,
        vmax=color_scale[1] if type(color_scale) == tuple else None,
        cmap=cmap,
        gridsize=40,
        edgecolors="white",
    )
    #set the font size to be the same as the axis label size
    cbar = plt.colorbar(f, ax=ax)
    cbar.ax.tick_params(labelsize=tick_label_size,
                        width=tick_line_width,
                        length=tick_line_length)
    cbar.outline.set_visible(False)

    ax.set_xlabel(xlabel, fontsize=axis_label_size)
    ax.set_ylabel(ylabel, fontsize=axis_label_size)
    ax.tick_params(axis="both", which="major", labelsize=tick_label_size)

    correlation = pearsonr(merged_df["other_population_frequency"], merged_df["stix_population_frequency"])
    r = correlation.statistic
    p = correlation.pvalue
    if title:
        ax.set_title(title, fontsize=axis_label_size, loc='left')
    print(f"r = {r:.2f}, p={p:.2e}")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines['bottom'].set_linewidth(axis_line_width)
    ax.spines['left'].set_linewidth(axis_line_width)

    ax.tick_params(axis='both',
                   which='major',
                   labelsize=axis_label_size,
                   width=tick_line_width,
                   length=tick_line_length)

    if fignum:
        ax.annotate(fignum,
                    xy=(.025, .975), xycoords='figure fraction',
                    horizontalalignment='left', verticalalignment='top',
                    fontsize=12)

    fig.tight_layout()
    fig.savefig(output, dpi=600)
    fig.savefig(output+".svg", format='svg',transparent=True)


if __name__ == "__main__":
    args = parse_args()
    plot_data(**vars(args))
