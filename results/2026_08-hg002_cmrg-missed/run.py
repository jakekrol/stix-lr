#!/usr/bin/env python3

import argparse
from cyvcf2 import VCF
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import numpy as np
import sys

parser = argparse.ArgumentParser(description="")
parser.add_argument("--needlr", default='../2026_07-hg002_cmrg-needlr/needLR_ov0.5/needlr_pop_freq.tsv', help="Path to the needlr table")
parser.add_argument("--svafotate", default="../2025_12-hg002_cmrg-svafotate/svafotate-hg002-cmrg-overlap_0.9_maxpopfreq.txt", help="Path to the svafotate table")
parser.add_argument("--stixlr", default="../2025_12-hg002_cmrg-stix_lr/hg002_cmrg.stix_lr.min_read_5.popfreq.tsv", help="Path to the stixlr table")
parser.add_argument("--query_vcf", default='../../data/2025_12-hg002-cmrg/HG002_GRCh38_difficult_medical_gene_SV_benchmark_v0.01_trusted_SVTYPE.addID.svafotate.vcf', help="Path to the query VCF file")
parser.add_argument("--out_prefix", default='hg002_cmrg', help="Prefix for the output files")
args = parser.parse_args()

LENGTH_BINS = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 5000, 10000, 15000, 20000, 10**9]
BIN_LABELS = [
    '0-100bp', '100-200bp', '200-300bp', '300-400bp', '400-500bp', '500-600bp',
    '600-700bp', '700-800bp', '800-900bp', '900-1kbp', '1k-5kbp', '5k-10kbp',
    '10k-15kbp', '15k-20kbp', '>20kbp'
]
STIX_SVID_COL='svid'
STIX_SAMPLE_COL='sample_count'
NEEDLR_SVID_COL='svid'
NEEDLR_AF_COL='allele_frequency'
SVAFOTATE_SVID_COL='svid'
SVAFOTATE_AF_COL='max_popfreq'

SVCALLSET="HG002 CMRG SVs"

XLABEL_TYPE_BAR='SV type'
XLABEL_LENGTH_BAR='SV length'


def main():
    df_stixlr = pd.read_csv(args.stixlr, sep='\t')
    df_needlr = pd.read_csv(args.needlr, sep='\t')
    df_svafotate = pd.read_csv(args.svafotate, sep='\t')

    df_stixlr_missed = df_stixlr[df_stixlr[STIX_SAMPLE_COL] == 0]
    df_stixlr_recovered = df_stixlr[df_stixlr[STIX_SAMPLE_COL] > 0]
    df_needlr_missed = df_needlr[df_needlr[NEEDLR_AF_COL] == 0]
    df_needlr_recovered = df_needlr[df_needlr[NEEDLR_AF_COL] > 0]
    df_svafotate_missed = df_svafotate[df_svafotate[SVAFOTATE_AF_COL] == 0]
    df_svafotate_recovered = df_svafotate[df_svafotate[SVAFOTATE_AF_COL] > 0]

    hg002_cmrg_ids = set(df_stixlr[STIX_SVID_COL]).union(set(df_needlr[NEEDLR_SVID_COL])).union(set(df_svafotate[SVAFOTATE_SVID_COL]))
    missed_stixlr = set(df_stixlr_missed[STIX_SVID_COL])
    recovered_stixlr = set(df_stixlr_recovered[STIX_SVID_COL])
    missed_needlr = set(df_needlr_missed[NEEDLR_SVID_COL])
    recovered_needlr = set(df_needlr_recovered[NEEDLR_SVID_COL])
    missed_svafotate = set(df_svafotate_missed[SVAFOTATE_SVID_COL])
    recovered_svafotate = set(df_svafotate_recovered[SVAFOTATE_SVID_COL])
    vcf = VCF(args.query_vcf)
    lengths_missed_stixlr = []
    lengths_recovered_stixlr = []
    type_missed_stixlr = []
    type_recovered_stixlr = []

    lengths_missed_needlr = []
    lengths_recovered_needlr = []
    type_missed_needlr = []
    type_recovered_needlr = []

    lengths_missed_svafotate = []
    lengths_recovered_svafotate = []
    type_missed_svafotate = []
    type_recovered_svafotate = []
    for variant in vcf:
        if variant.ID in missed_stixlr:
            lengths_missed_stixlr.append(variant.INFO.get('SVLEN'))
            type_missed_stixlr.append(variant.INFO.get('SVTYPE'))
        elif variant.ID in recovered_stixlr:
            lengths_recovered_stixlr.append(variant.INFO.get('SVLEN'))
            type_recovered_stixlr.append(variant.INFO.get('SVTYPE'))
        
        if variant.ID in missed_needlr:
            lengths_missed_needlr.append(variant.INFO.get('SVLEN'))
            type_missed_needlr.append(variant.INFO.get('SVTYPE'))
        elif variant.ID in recovered_needlr:
            lengths_recovered_needlr.append(variant.INFO.get('SVLEN'))
            type_recovered_needlr.append(variant.INFO.get('SVTYPE'))

        if variant.ID in missed_svafotate:
            lengths_missed_svafotate.append(variant.INFO.get('SVLEN'))
            type_missed_svafotate.append(variant.INFO.get('SVTYPE'))
        elif variant.ID in recovered_svafotate:
            lengths_recovered_svafotate.append(variant.INFO.get('SVLEN'))
            type_recovered_svafotate.append(variant.INFO.get('SVTYPE'))

    type_missed_counts_stixlr = Counter(type_missed_stixlr)
    type_recovered_counts_stixlr = Counter(type_recovered_stixlr)
    type_missed_counts_needlr = Counter(type_missed_needlr)
    type_recovered_counts_needlr = Counter(type_recovered_needlr)
    type_missed_counts_svafotate = Counter(type_missed_svafotate)
    type_recovered_counts_svafotate = Counter(type_recovered_svafotate)

    lengths_missed_stixlr = [abs(l) for l in lengths_missed_stixlr]
    lengths_recovered_stixlr = [abs(l) for l in lengths_recovered_stixlr]
    lengths_missed_needlr = [abs(l) for l in lengths_missed_needlr]
    lengths_recovered_needlr = [abs(l) for l in lengths_recovered_needlr]
    lengths_missed_svafotate = [abs(l) for l in lengths_missed_svafotate]
    lengths_recovered_svafotate = [abs(l) for l in lengths_recovered_svafotate]
            
    ### stixlr plots
    if len(lengths_missed_stixlr) > 0:
        fig, ax = plt.subplots(figsize=(6, 5))
        counts, edges = np.histogram(lengths_missed_stixlr, bins=LENGTH_BINS)
        bars = ax.bar(BIN_LABELS, counts, color='red')
        ax.bar_label(bars)
        ax.set_title(f'{SVCALLSET} STIX-LR population frequency = 0')
        ax.set_xlabel(XLABEL_LENGTH_BAR)
        ax.set_ylabel('Count')
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(f"{args.out_prefix}-stixlr-missed-length-bar.png")

    if len(lengths_recovered_stixlr) > 0:
        fig, ax = plt.subplots(figsize=(6, 5))
        counts, edges = np.histogram(lengths_recovered_stixlr, bins=LENGTH_BINS)
        bars = ax.bar(BIN_LABELS, counts, color='blue')
        ax.bar_label(bars)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_title(f'{SVCALLSET} STIX-LR population frequency > 0')
        ax.set_xlabel(XLABEL_LENGTH_BAR)
        ax.set_ylabel('Count')
        plt.tight_layout()
        plt.savefig(f"{args.out_prefix}-stixlr-recovered-length-bar.png")

    if len(type_missed_counts_stixlr.values()) > 0:
        fig, ax = plt.subplots(figsize=(6, 5))
        bars = ax.bar(type_missed_counts_stixlr.keys(), type_missed_counts_stixlr.values(), color='red')
        ax.bar_label(bars)
        ax.set_title(f'{SVCALLSET} STIX-LR population frequency = 0')
        ax.set_xlabel(XLABEL_TYPE_BAR)
        ax.set_ylabel('Count')
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(f"{args.out_prefix}-stixlr-missed-type-bar.png")
    
    if len(type_recovered_counts_stixlr.values()) > 0:
        fig, ax = plt.subplots(figsize=(6, 5))
        bars = ax.bar(type_recovered_counts_stixlr.keys(), type_recovered_counts_stixlr.values(), color='blue')
        ax.bar_label(bars)
        ax.set_title(f'{SVCALLSET} STIX-LR population frequency > 0')
        ax.set_xlabel(XLABEL_TYPE_BAR)
        ax.set_ylabel('Count')
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(f"{args.out_prefix}-stixlr-recovered-type-bar.png")

    ### needlr plots
    if len(lengths_missed_needlr) > 0:
        fig, ax = plt.subplots(figsize=(6, 5))
        counts, edges = np.histogram(lengths_missed_needlr, bins=LENGTH_BINS)
        bars = ax.bar(BIN_LABELS, counts, color='red')
        ax.bar_label(bars)
        ax.set_title(f'{SVCALLSET} needLR population frequency = 0')
        ax.set_xlabel(XLABEL_LENGTH_BAR)
        ax.set_ylabel('Count')
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(f"{args.out_prefix}-needlr-missed-length-bar.png")

    if len(lengths_recovered_needlr) > 0:
        fig, ax = plt.subplots(figsize=(6, 5))
        counts, edges = np.histogram(lengths_recovered_needlr, bins=LENGTH_BINS)
        bars = ax.bar(BIN_LABELS, counts, color='blue')
        ax.bar_label(bars)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_title(f'{SVCALLSET} needLR population frequency > 0')
        ax.set_xlabel(XLABEL_LENGTH_BAR)
        ax.set_ylabel('Count')
        plt.tight_layout()
        plt.savefig(f"{args.out_prefix}-needlr-recovered-length-bar.png")

    if len(type_missed_counts_needlr.values()) > 0:
        fig, ax = plt.subplots(figsize=(6, 5))
        bars = ax.bar(type_missed_counts_needlr.keys(), type_missed_counts_needlr.values(), color='red')
        ax.bar_label(bars)
        ax.set_title(f'{SVCALLSET} needLR population frequency = 0')
        ax.set_xlabel(XLABEL_TYPE_BAR)
        ax.set_ylabel('Count')
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(f"{args.out_prefix}-needlr-missed-type-bar.png")
    
    if len(type_recovered_counts_needlr.values()) > 0:
        fig, ax = plt.subplots(figsize=(6, 5))
        bars = ax.bar(type_recovered_counts_needlr.keys(), type_recovered_counts_needlr.values(), color='blue')
        ax.bar_label(bars)
        ax.set_title(f'{SVCALLSET} needLR population frequency > 0')
        ax.set_xlabel(XLABEL_TYPE_BAR)
        ax.set_ylabel('Count')
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(f"{args.out_prefix}-needlr-recovered-type-bar.png")

    ### svafotate plots
    if len(lengths_missed_svafotate) > 0:
        fig, ax = plt.subplots(figsize=(6, 5))
        counts, edges = np.histogram(lengths_missed_svafotate, bins=LENGTH_BINS)
        bars = ax.bar(BIN_LABELS, counts, color='red')
        ax.bar_label(bars)
        ax.set_title(f'{SVCALLSET} SVAFotate population frequency = 0')
        ax.set_xlabel(XLABEL_LENGTH_BAR)
        ax.set_ylabel('Count')
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(f"{args.out_prefix}-svafotate-missed-length-bar.png")

    if len(lengths_recovered_svafotate) > 0:
        fig, ax = plt.subplots(figsize=(6, 5))
        counts, edges = np.histogram(lengths_recovered_svafotate, bins=LENGTH_BINS)
        bars = ax.bar(BIN_LABELS, counts, color='blue')
        ax.bar_label(bars)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_title(f'{SVCALLSET} SVAFotate population frequency > 0')
        ax.set_xlabel(XLABEL_LENGTH_BAR)
        ax.set_ylabel('Count')
        plt.tight_layout()
        plt.savefig(f"{args.out_prefix}-svafotate-recovered-length-bar.png")

    if len(type_missed_counts_svafotate.values()) > 0:
        fig, ax = plt.subplots(figsize=(6, 5))
        bars = ax.bar(type_missed_counts_svafotate.keys(), type_missed_counts_svafotate.values(), color='red')
        ax.bar_label(bars)
        ax.set_title(f'{SVCALLSET} SVAFotate population frequency = 0')
        ax.set_xlabel(XLABEL_TYPE_BAR)
        ax.set_ylabel('Count')
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(f"{args.out_prefix}-svafotate-missed-type-bar.png")
    
    if len(type_recovered_counts_svafotate.values()) > 0:
        fig, ax = plt.subplots(figsize=(6, 5))
        bars = ax.bar(type_recovered_counts_svafotate.keys(), type_recovered_counts_svafotate.values(), color='blue')
        ax.bar_label(bars)
        ax.set_title(f'{SVCALLSET} SVAFotate population frequency > 0')
        ax.set_xlabel(XLABEL_TYPE_BAR)
        ax.set_ylabel('Count')
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(f"{args.out_prefix}-svafotate-recovered-type-bar.png")
    
    ### stats
    stixlr_recall = len(recovered_stixlr) / len(hg002_cmrg_ids) 
    needlr_recall = len(recovered_needlr) / len(hg002_cmrg_ids)
    svafotate_recall = len(recovered_svafotate) / len(hg002_cmrg_ids)
    with open(f"{args.out_prefix}-recall.tsv", 'w') as f:
        f.write("Method\tRecall\n")
        f.write(f"STIX-LR\t{stixlr_recall:.4f}\n")
        f.write(f"needLR\t{needlr_recall:.4f}\n")
        f.write(f"SVAFotate\t{svafotate_recall:.4f}\n")
    with open(f"{args.out_prefix}-type-fractions.tsv", 'w') as f:
        f.write("Method\tMissed_INS\tMissed_DEL\tRecovered_INS\tRecovered_DEL\n")
        if len(missed_stixlr) > 0:
            frac_ins_missed_stixlr = type_missed_counts_stixlr.get('INS', 0) / len(missed_stixlr)
            frac_del_missed_stixlr = type_missed_counts_stixlr.get('DEL', 0) / len(missed_stixlr)
            frac_ins_recovered_stixlr = type_recovered_counts_stixlr.get('INS', 0) / len(recovered_stixlr)
            frac_del_recovered_stixlr = type_recovered_counts_stixlr.get('DEL', 0) / len(recovered_stixlr)
            f.write(f"STIX-LR\t{frac_ins_missed_stixlr:.4f}\t{frac_del_missed_stixlr:.4f}\t{frac_ins_recovered_stixlr:.4f}\t{frac_del_recovered_stixlr:.4f}\n")
        if len(missed_needlr) > 0:
            frac_ins_missed_needlr = type_missed_counts_needlr.get('INS', 0) / len(missed_needlr)
            frac_del_missed_needlr = type_missed_counts_needlr.get('DEL', 0) / len(missed_needlr)
            frac_ins_recovered_needlr = type_recovered_counts_needlr.get('INS', 0) / len(recovered_needlr)
            frac_del_recovered_needlr = type_recovered_counts_needlr.get('DEL', 0) / len(recovered_needlr)
            f.write(f"needLR\t{frac_ins_missed_needlr:.4f}\t{frac_del_missed_needlr:.4f}\t{frac_ins_recovered_needlr:.4f}\t{frac_del_recovered_needlr:.4f}\n")
        if len(missed_svafotate) > 0:
            frac_ins_missed_svafotate = type_missed_counts_svafotate.get('INS', 0) / len(missed_svafotate)
            frac_del_missed_svafotate = type_missed_counts_svafotate.get('DEL', 0) / len(missed_svafotate)
            frac_ins_recovered_svafotate = type_recovered_counts_svafotate.get('INS', 0) / len(recovered_svafotate)
            frac_del_recovered_svafotate = type_recovered_counts_svafotate.get('DEL', 0) / len(recovered_svafotate)
            f.write(f"SVAFotate\t{frac_ins_missed_svafotate:.4f}\t{frac_del_missed_svafotate:.4f}\t{frac_ins_recovered_svafotate:.4f}\t{frac_del_recovered_svafotate:.4f}\n")
    


if __name__ == "__main__":
    main()