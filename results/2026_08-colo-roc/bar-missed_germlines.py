#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser(description="Bar plot num. COLO germline SVs with 0 pop. freq.")
parser.add_argument(
    "--input",
    default="./missed_germlines.tsv"
)
parser.add_argument(
    "--output",
    default="bar-missed_germlines.png"
)
# plot
parser.add_argument(
    "--figsize",
    default=(6,5)
)
parser.add_argument(
    "--title",
    default="COLO germline SVs"
)
parser.add_argument(
    "--ymax",
    default=1
)
args = parser.parse_args()

def main():
    df = pd.read_csv(args.input, sep="\t")
    y = df['frac_zero_popfreq_germline']
    x = [
        'STIX-LR;MR=1',
        'STIX-LR;MR=5',
        'SVAFotate;OV=0.5',
        'SVAFotate;OV=0.7',
        'SVAFotate;OV=0.9',
        'NeedLR;OV=0.5',
        'NeedLR;OV=0.7',
        'NeedLR;OV=0.9'
    ]
    fig, ax = plt.subplots(figsize=args.figsize)
    bar = ax.bar(x, y)
    ax.bar_label(bar,padding=3)
    ax.set_ylabel("Fraction germline SVs with 0 pop. freq.")
    ax.set_title(args.title, loc="left")
    ax.set_ylim(0, args.ymax)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.savefig(args.output, dpi=300)

if __name__ == "__main__":
    main()
