#!/usr/bin/env python3
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt


p = argparse.ArgumentParser(
    description="Plot violin/density plots for one-column data files."
)
p.add_argument(
    "-i",
    "--inputs",
    required=True,
    help=(
        "Comma-separated list of files. "
        "Each file must have a single numeric column (no header)."
    ),
)
p.add_argument(
    "-o",
    "--output",
    required=True,
    help="Output image file (e.g. density.png).",
)
p.add_argument(
    "--title",
    default="Density / Violin plots",
    help="Plot title.",
)
p.add_argument(
    "--names",
    help=(
        "Optional comma-separated list of display names for each input file. "
        "Must have the same number of entries as --inputs if provided."
    ),
)
p.add_argument(
    "--fontsize",
    type=int,
    default=10,
    help="Base font size.",
)
p.add_argument(
    "--figsize",
    type=float,
    nargs=2,
    default=(6, 5),
    metavar=("W", "H"),
    help="Figure size in inches, e.g. --figsize 6 5",
)
p.add_argument(
    "-x",
    "--xlabel",
    default="Dataset",
    help="X-axis label."
)
p.add_argument(
    "-y",
    "--ylabel",
    default="Value",
    help="Y-axis label."
)
p.add_argument(
    "--half_violin",
    action="store_true",
    help="Plot only one side of each violin (no mirror).",
)
p.add_argument(
    "--show_median",
    action="store_true",
    help="Show median line in violin plots."
)
p.add_argument(
    "--y_min",
    type=float,
    default=None,
    help="Minimum y-axis limit (default: auto)."
)
p.add_argument(
    "--y_max",
    type=float,
    default=None,
    help="Maximum y-axis limit (default: auto)."
)

def load_values(path):
    data = np.loadtxt(path, dtype=float)
    # allow both 1D and single-column 2D
    if data.ndim == 2:
        if data.shape[1] != 1:
            raise ValueError(
                f"File '{path}' must have exactly one column, got shape {data.shape}."
            )
        data = data[:, 0]
    return np.asarray(data, dtype=float)


def main():
    args = p.parse_args()

    plt.figure(figsize=tuple(args.figsize))
    plt.rcParams.update({"font.size": args.fontsize})
    ax = plt.gca()

    input_paths = [s.strip() for s in args.inputs.split(",") if s.strip()]
    if not input_paths:
        raise ValueError("No valid input files provided to --inputs.")

    if args.names is not None:
        names = [n.strip() for n in args.names.split(",")]
        if len(names) != len(input_paths):
            raise ValueError(
                f"--names has {len(names)} entries but --inputs has {len(input_paths)} files."
            )
    else:
        names = None

    datasets = []
    labels = []

    for idx, path in enumerate(input_paths):
        values = load_values(path)
        datasets.append(values)
        label = names[idx] if names is not None else os.path.basename(path)
        labels.append(label)

    # Pre-compute medians for optional custom median lines
    medians = [np.median(d) for d in datasets]

    positions = np.arange(1, len(datasets) + 1)

    vp = ax.violinplot(
        datasets,
        positions=positions,
        showmeans=False,
        showmedians=False if (args.half_violin or not args.show_median) else True,
        showextrema=False,
    )

    # Optionally collapse one side of each violin so it is not mirrored
    if args.half_violin:
        for body in vp["bodies"]:
            verts = body.get_paths()[0].vertices
            xs = verts[:, 0]
            center = (xs.max() + xs.min()) / 2.0
            # Collapse everything left of the center onto the center
            verts[xs < center, 0] = center

    # Optionally draw median lines. For half violins, restrict the line
    # to the visible (non-collapsed) half so it doesn't span both sides.
    if args.show_median and args.half_violin:
        for i, (body, median) in enumerate(zip(vp["bodies"], medians)):
            verts = body.get_paths()[0].vertices
            xs = verts[:, 0]
            x_left = positions[i]
            # make x_right a bit smaller so line is fully inside violin
            x_right = xs.max() - (xs.max() - xs.min()) * 0.25
            ax.hlines(median, x_left, x_right, colors="black", linewidth=1)

    # Set x-axis labels corresponding to each dataset/shifted position
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    # remove top and right spines for a cleaner look
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # left-justify title
    ax.set_title(args.title, loc="left", fontsize=args.fontsize + 2)

    ax.set_xlabel(args.xlabel)
    ax.set_ylabel(args.ylabel)
    if args.y_min is not None:
        ax.set_ylim(bottom=args.y_min)
    if args.y_max is not None:
        ax.set_ylim(top=args.y_max)


    plt.tight_layout()
    plt.savefig(args.output, dpi=300)


if __name__ == "__main__":
    main()
