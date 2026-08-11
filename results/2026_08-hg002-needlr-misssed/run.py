#!/usr/bin/env python3

import argparse
from cyvcf2 import VCF
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import numpy as np
import sys

parser = argparse.ArgumentParser(description="")
parser.add_argument("--table_needlr", default='../2026_07-hg002-needlr/needLR_ov0.5/needlr_pop_freq.tsv', help="Path to the needlr table")
parser.add_argument("--query_vcf", default='../../data/2026_07-hg002-svs/GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.AF.END.gt50bp.vcf.gz', help="Path to the query VCF file")
parser.add_argument("--out_prefix", default='hg002-needlr', help="Prefix for the output files")
args = parser.parse_args()

LENGTH_BINS = [50, 100, 500, 1000, 5000, 10000, int(10 ** 5), int(10 ** 6), int(10 ** 9)]
# [50, 100), [100, 500), [500, 1000), [1000, 5000), [5000, 10000), [10000, 10^5), [10^5, 10^6), [10^6, 10^9)]
BIN_LABELS = ['50-100bp', '100-500bp', '500-1kbp', '1k-5kbp', '5k-10kbp', '10k-100kbp', '100k-1Mbp', '>1Mbp']

def main():
    df = pd.read_csv(args.table_needlr, sep='\t')
    missed_svs = set(df[df['population_frequency'] == 0].svid.tolist())
    recovered_svs = set(df[df['population_frequency'] > 0].svid.tolist())
    vcf = VCF(args.query_vcf)
    lengths_missed = []
    lengths_recovered = []
    type_missed = []
    type_recovered = []
    for variant in vcf:
        if variant.ID in missed_svs:
            lengths_missed.append(variant.INFO.get('SVLEN'))
            type_missed.append(variant.INFO.get('SVTYPE'))
        elif variant.ID in recovered_svs:
            lengths_recovered.append(variant.INFO.get('SVLEN'))
            type_recovered.append(variant.INFO.get('SVTYPE'))
    type_missed_counts = Counter(type_missed)
    type_recovered_counts = Counter(type_recovered)
    lengths_missed = [abs(l) for l in lengths_missed]
    lengths_recovered = [abs(l) for l in lengths_recovered]
            
    fig, ax = plt.subplots(figsize=(6, 5))
    counts, edges = np.histogram(lengths_missed, bins=LENGTH_BINS)
    ax.bar(BIN_LABELS, counts, color='red')
    ax.set_title('HG002 SVs needLR population frequency = 0')
    ax.set_xlabel('SV Length')
    ax.set_ylabel('Count')
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"{args.out_prefix}-missed-length-bar.png")

    fig, ax = plt.subplots(figsize=(6, 5))
    counts, edges = np.histogram(lengths_recovered, bins=LENGTH_BINS)
    ax.bar(BIN_LABELS, counts, color='blue')
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title('HG002 SVs needLR population frequency > 0')
    ax.set_xlabel('SV Length')
    ax.set_ylabel('Count')
    plt.tight_layout()
    plt.savefig(f"{args.out_prefix}-recovered-length-bar.png")

    fig, ax = plt.subplots(figsize=(6, 5))
    bars = ax.bar(type_missed_counts.keys(), type_missed_counts.values(), color='red')
    ax.bar_label(bars)
    ax.set_title('HG002 SVs needLR population frequency = 0')
    ax.set_xlabel('SV type')
    ax.set_ylabel('Count')
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"{args.out_prefix}-missed-type-bar.png")
    
    fig, ax = plt.subplots(figsize=(6, 5))
    bars = ax.bar(type_recovered_counts.keys(), type_recovered_counts.values(), color='blue')
    ax.bar_label(bars)
    ax.set_title('HG002 SVs needLR population frequency > 0')
    ax.set_xlabel('SV type')
    ax.set_ylabel('Count')
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"{args.out_prefix}-recovered-type-bar.png")


if __name__ == "__main__":
    main()