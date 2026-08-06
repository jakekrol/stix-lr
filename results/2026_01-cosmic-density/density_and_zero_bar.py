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
    help="Base output image file name (used as prefix for the two plots).",
)
p.add_argument(
    "--output_medians",
    default="medians.tsv",
    help="Output file for median values.",
)
p.add_argument(
    "--output_nonzero_fractions",
    default="nonzero_fractions.tsv",
    help="Output file for non-zero fractions.",
)
p.add_argument(
    "--output_near_zero_fractions",
    default="near_zero_fractions.tsv",
    help="Output file for near-zero fractions.",
)
p.add_argument(
    "--output_zero_fractions",
    default="zero_fractions.tsv",
    help="Output file for zero fractions."
)
p.add_argument(
    "--output_nonzero_variannce",
    default="nonzero_variance.tsv",
    help="Output file for non-zero variance.",
)
p.add_argument(
    "--near_zero_upper",
    type=float,
    default=0.01,
    help="Upper bound for near-zero values."
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
    "--ylabel_density",
    default="Population frequency (non-zero)",
    help="Y-axis label."
)
p.add_argument(
    "--ylabel_bar",
    default="Num. SVs with population frequency = 0",
    help="Y-axis label for bar plot."
)
p.add_argument(
    "--half_violin",
    action="store_true",
    help="Plot only one side of each violin (no mirror).",
)
p.add_argument(
    "--show_median",
    action="store_true",
    help="Show median line in violin plots.",
)
p.add_argument(
    "--title_bar", 
    default="COSMIC SVs",
    help="Title for the bar plot."
)
p.add_argument(
    "--title_violin", 
    default="COSMIC SVs",
    help="Title for the violin plot."
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

    plt.rcParams.update({"font.size": args.fontsize})

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
    print("Input files and labels:")
    for idx, path in enumerate(input_paths):
        label = names[idx] if names is not None else os.path.basename(path)
        print(f"  {idx+1}. {label}: {path}")

    datasets = []
    labels = []
    zero_counts = []
    nonzero_datasets = []
    nonzero_medians = []
    nonzero_fractions = []
    near_zero_fractions = []
    zero_fractions = []
    nonzero_variances = []

    for idx, path in enumerate(input_paths):
        print(f"Loading data from '{path}'...")
        v = load_values(path)
        datasets.append(v)
        labels.append(names[idx] if names is not None else os.path.basename(path))
        zero_counts.append(int((v == 0).sum()))
        nonzero_vals = v[v != 0]
        near_zero_vals = v[(v > 0) & (v <= args.near_zero_upper)]
        near_zero_fractions.append(len(near_zero_vals) / len(v) if len(v) > 0 else np.nan)
        zero_fractions.append(len(v[v == 0]) / len(v) if len(v) > 0 else np.nan)
        nonzero_datasets.append(nonzero_vals)
        nonzero_medians.append(float(np.median(nonzero_vals)) if len(nonzero_vals) > 0 else np.nan)
        nonzero_fractions.append(len(nonzero_vals) / len(v) if len(v) > 0 else np.nan)
        nonzero_variances.append(float(np.var(nonzero_vals)) if len(nonzero_vals) > 0 else np.nan)

    def draw_violins(ax):
        pos = np.arange(1, len(labels) + 1)
        data = [d for d in nonzero_datasets if len(d) > 0]
        if not data:
            raise ValueError("All datasets are zero-only; no non-zero values to plot.")
        # keep positions aligned with labels, but skip empty datasets
        used_pos = [p for p, d in zip(pos, nonzero_datasets) if len(d) > 0]
        vp = ax.violinplot(
            data,
            positions=used_pos,
            showmeans=False,
            showmedians=args.show_median,
            showextrema=False,
        )
        if args.half_violin:
            for b in vp["bodies"]:
                verts = b.get_paths()[0].vertices
                xs = verts[:, 0]
                c = (xs.max() + xs.min()) / 2.0
                verts[xs < c, 0] = c
        ax.set_xticks(pos)
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_xlabel(args.xlabel)

    # save bar plot separately
    bar_output = args.output if args.output.endswith((".png", ".pdf", ".svg")) else f"{args.output}_bar.png"
    if not bar_output.endswith((".png", ".pdf", ".svg")):
        bar_output = f"{bar_output}_bar.png"

    violin_output = args.output if args.output.endswith((".png", ".pdf", ".svg")) else f"{args.output}_violin.png"
    if not violin_output.endswith((".png", ".pdf", ".svg")):
        violin_output = f"{violin_output}_violin.png"

    if bar_output == violin_output:
        bar_output = f"{os.path.splitext(args.output)[0]}_bar.png"
        violin_output = f"{os.path.splitext(args.output)[0]}_violin.png"

    fig_bar, ax_bar = plt.subplots(figsize=(6, 5))
    ax_bar.set_title(args.title_bar, loc='left')
    x = np.arange(len(labels))
    ax_bar.bar(x, zero_counts)
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(labels, rotation=45, ha="right")
    ax_bar.set_ylabel(args.ylabel_bar)
    ax_bar.spines["top"].set_visible(False)
    ax_bar.spines["right"].set_visible(False)
    fig_bar.tight_layout()
    fig_bar.savefig(bar_output, dpi=300)
    plt.close(fig_bar)

    fig_violin, ax_violin = plt.subplots(figsize=(6, 5))
    ax_violin.set_title(args.title_violin, loc='left')
    draw_violins(ax_violin)
    ax_violin.set_ylabel(args.ylabel_density)
    ax_violin.spines["top"].set_visible(False)
    ax_violin.spines["right"].set_visible(False)
    fig_violin.tight_layout()
    fig_violin.savefig(violin_output, dpi=300)
    plt.close(fig_violin)

    with open(args.output_medians, "w") as fh:
        fh.write("tool\tmedian_nonzero\n")
        for label, median in zip(labels, nonzero_medians):
            fh.write(f"{label}\t{median}\n")
    with open(args.output_nonzero_fractions, "w") as fh:
        fh.write("tool\tnonzero_fraction\n")
        for label, fraction in zip(labels, nonzero_fractions):
            fh.write(f"{label}\t{fraction}\n")
    with open(args.output_near_zero_fractions, "w") as fh:
        fh.write("tool\tnear_zero_fraction\n")
        for label, fraction in zip(labels, near_zero_fractions):
            fh.write(f"{label}\t{fraction}\n")
    with open(args.output_zero_fractions, "w") as fh:
        fh.write("tool\tzero_fraction\n")
        for label, fraction in zip(labels, zero_fractions):
            fh.write(f"{label}\t{fraction}\n")
    with open(args.output_nonzero_variannce, "w") as fh:
        fh.write("tool\tnonzero_variance\n")
        for label, variance in zip(labels, nonzero_variances):
            fh.write(f"{label}\t{variance}\n")


if __name__ == "__main__":
    main()
