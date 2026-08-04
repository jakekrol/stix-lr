#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Bar plot hg002 cmrg recall for all tools")
# inputs
parser.add_argument(
    "--stixlr_mr1",
    default="../2025_12-hg002_cmrg-stix_lr/hg002_cmrg.stix_lr.min_read_1.popfreq.tsv"
)
parser.add_argument(
    "--stixlr_mr5",
    default="../2025_12-hg002_cmrg-stix_lr/hg002_cmrg.stix_lr.min_read_5.popfreq.tsv"
)
parser.add_argument(
    "--svafotate_ov05",
    default="../2025_12-hg002_cmrg-svafotate/svafotate-hg002-cmrg-overlap_0.5_maxpopfreq.txt"
)
parser.add_argument(
    "--svafotate_ov07",
    default="../2025_12-hg002_cmrg-svafotate/svafotate-hg002-cmrg-overlap_0.7_maxpopfreq.txt"
)
parser.add_argument(
    "--svafotate_ov09",
    default="../2025_12-hg002_cmrg-svafotate/svafotate-hg002-cmrg-overlap_0.9_maxpopfreq.txt"
)
parser.add_argument(
    "--needlr_ov05",
    default="../2026_07-hg002_cmrg-needlr/needLR_ov0.5/needlr_pop_freq.tsv"
)
parser.add_argument(
    "--needlr_ov07",
    default="../2026_07-hg002_cmrg-needlr/needLR_ov0.7/needlr_pop_freq.tsv"
)
parser.add_argument(
    "--needlr_ov09",
    default="../2026_07-hg002_cmrg-needlr/needLR_ov0.9/needlr_pop_freq.tsv"
)
# params
parser.add_argument(
    "--stix_samples",
    default=1108
)
# plot
parser.add_argument(
    "--figsize",
    default = (6,5)
)
parser.add_argument(
    "--output",
    default="hg002_cmrg-recall-bar.png"
)
parser.add_argument(
    "--title",
    default="HG002 CMRG SVs"
)
args = parser.parse_args()

def main():
    stixlr_mr1 = pd.read_csv(args.stixlr_mr1, sep="\t")
    stixlr_mr1 = (stixlr_mr1['sample_count'] / args.stix_samples).values
    stixlr_mr1_recall = (stixlr_mr1 > 0).sum() / len(stixlr_mr1)
    stixlr_mr5 = pd.read_csv(args.stixlr_mr5, sep="\t")
    stixlr_mr5 = (stixlr_mr5['sample_count'] / args.stix_samples).values
    stixlr_mr5_recall = (stixlr_mr5 > 0).sum() / len(stixlr_mr5)

    svafotate_ov05 = pd.read_csv(args.svafotate_ov05, sep="\t")
    svafotate_ov05 = (svafotate_ov05['max_popfreq']).values
    svafotate_ov05_recall = (svafotate_ov05 > 0).sum() / len(svafotate_ov05)
    svafotate_ov07 = pd.read_csv(args.svafotate_ov07, sep="\t")
    svafotate_ov07 = (svafotate_ov07['max_popfreq']).values
    svafotate_ov07_recall = (svafotate_ov07 > 0).sum() / len(svafotate_ov07)
    svafotate_ov09 = pd.read_csv(args.svafotate_ov09, sep="\t")
    svafotate_ov09 = (svafotate_ov09['max_popfreq']).values
    svafotate_ov09_recall = (svafotate_ov09 > 0).sum() / len(svafotate_ov09)

    needlr_ov05 = pd.read_csv(args.needlr_ov05, sep="\t")
    needlr_ov05 = (needlr_ov05['population_frequency']).values
    needlr_ov05_recall = (needlr_ov05 > 0).sum() / len(needlr_ov05)
    needlr_ov07 = pd.read_csv(args.needlr_ov07, sep="\t")
    needlr_ov07 = (needlr_ov07['population_frequency']).values
    needlr_ov07_recall = (needlr_ov07 > 0).sum() / len(needlr_ov07)
    needlr_ov09 = pd.read_csv(args.needlr_ov09, sep="\t")
    needlr_ov09 = (needlr_ov09['population_frequency']).values
    needlr_ov09_recall = (needlr_ov09 > 0).sum() / len(needlr_ov09)


    # plot recall
    fig, ax = plt.subplots(figsize=args.figsize)
    x = [
        'STIX-LR;MR=1',
        'STIX-LR;MR=5',
        'SVAFotate;OV=0.5',
        'SVAFotate;OV=0.7',
        'SVAFotate;OV=0.9',
        'needLR;OV=0.5',
        'needLR;OV=0.7',
        'needLR;OV=0.9'
    ]
    y = [
        stixlr_mr1_recall,
        stixlr_mr5_recall,
        svafotate_ov05_recall,
        svafotate_ov07_recall,
        svafotate_ov09_recall,
        needlr_ov05_recall,
        needlr_ov07_recall,
        needlr_ov09_recall
    ]
    ax.bar(x, y)
    ax.set_ylabel("Recall")
    ax.set_title(args.title, loc='left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(args.output, dpi=300)

if __name__ == "__main__":
    main()