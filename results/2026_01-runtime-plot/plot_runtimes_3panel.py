#!/usr/bin/env python3
import argparse

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def parse_args():
    p = argparse.ArgumentParser(
        description="Plot runtimes in three horizontal bar-chart panels."
    )
    p.add_argument(
        "--input",
        required=True,
        help="Input TSV file with columns: dataset_method, runtime.",
    )
    p.add_argument(
        "--output",
        required=True,
        help="Output image file (e.g. runtimes.png).",
    )
    p.add_argument(
        "--figsize",
        type=float,
        nargs=2,
        default=(8, 6),
        metavar=("W", "H"),
        help="Figure size in inches (width height).",
    )
    p.add_argument(
        "--fontsize",
        type=float,
        default=8,
        help="Base font size for labels.",
    )
    return p.parse_args()


def get_dataset(label: str) -> str | None:
    """Return high-level dataset name from dataset_method string."""
    s = label.lower()
    if s.startswith("colo|"):
        return "COLO"
    if s.startswith("hg002 cmrg|"):
        return "HG002 CMRG"
    if s.startswith("cosmic|"):
        return "COSMIC"
    return None


def main():
    args = parse_args()

    df = pd.read_csv(args.input, sep="\t")

    # Determine which high-level dataset each row belongs to
    df["dataset"] = df["dataset_method"].apply(get_dataset)
    df = df.dropna(subset=["dataset"])  # drop rows that don't match

    # Compute log10 runtime
    df["log10_runtime"] = np.log10(df["runtime"].astype(float))

    datasets = ["COLO", "HG002 CMRG", "COSMIC"]

    fig, axes = plt.subplots(
        3,
        1,
        figsize=tuple(args.figsize),
        sharex=True,
        constrained_layout=True,
    )

    for ax, name in zip(axes, datasets):
        sub = df[df["dataset"] == name]
        if sub.empty:
            ax.set_visible(False)
            continue

        # Sort by runtime for a sensible ordering
        sub = sub.sort_values("runtime")

        labels = sub["dataset_method"].tolist()
        x = sub["log10_runtime"].to_numpy()
        y_pos = np.arange(len(labels))

        ax.barh(y_pos, x, color="black")
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels, fontsize=args.fontsize)
        ax.set_title(name, fontsize=args.fontsize + 1)

    axes[-1].set_xlabel("log10 runtime (s)", fontsize=args.fontsize)

    plt.savefig(args.output, dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
