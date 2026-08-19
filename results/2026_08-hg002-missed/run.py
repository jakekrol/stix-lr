#!/usr/bin/env python3

import argparse
from cyvcf2 import VCF
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import numpy as np
import sys

parser = argparse.ArgumentParser(description="")
parser.add_argument("--needlr", default='../2026_07-hg002-needlr/needLR_ov0.5/needlr_pop_freq.tsv', help="Path to the needlr table")
parser.add_argument("--svafotate", default="../2026_08-hg002-svafotate/svafotate-hg002_overlap_0.9_maxpopfreq.txt", help="Path to the svafotate table")
parser.add_argument("--stixlrmr5", default="../2026_08-hg002-stix_lr/hg002-stix_lr-min_read_5.popfreq.tsv", help="Path to the stixlr table")
parser.add_argument("--stixlrmr1", default="../2026_08-hg002-stix_lr/hg002-stix_lr-min_read_1.popfreq.tsv", help="Path to the stixlr table")
parser.add_argument("--query_vcf", default='../../data/2026_07-hg002-svs/GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.AF.END.gt50bp.vcf.gz', help="Path to the query VCF file")
parser.add_argument("--out_prefix", default='hg002', help="Prefix for the output files")
parser.add_argument("--figsize", default=(6, 5), type=lambda s: tuple(map(int, s.split(','))), help="Figure size for the plots (width,height)")
parser.add_argument("--cached_data", default=None)
args = parser.parse_args()

LENGTH_BINS = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 5000, 10000, 15000, 20000, 10**9]
BIN_LABELS = [
    '0-100bp', '100-200bp', '200-300bp', '300-400bp', '400-500bp', '500-600bp',
    '600-700bp', '700-800bp', '800-900bp', '900-1kbp', '1k-5kbp', '5k-10kbp',
    '10k-15kbp', '15k-20kbp', '>20kbp'
]
STIX_SVID_COL='SVID'
STIX_SAMPLE_COL='STIX_SAMPLES'
NEEDLR_SVID_COL='svid'
NEEDLR_AF_COL='allele_frequency'
SVAFOTATE_SVID_COL='svid'
SVAFOTATE_AF_COL='max_popfreq'

SVCALLSET="HG002 SVs"

XLABEL_TYPE_BAR='SV type'
YLABEL_TYPE_BAR='Count'
XLABEL_LENGTH_BAR='SV length'
YLABEL_LENGTH_BAR='Count'

def plot_sv_type_bar_chart(data, title, xlabel, ylabel, output_file, color, figsize=(6,5)):
    data = dict(sorted(data.items()))
    fig, ax = plt.subplots(figsize=figsize)
    labels = data.keys()
    values = data.values()
    bars = ax.bar(labels, values, color=color)
    ax.bar_label(bars, labels=[f'{v}' for v in values], padding=3)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def plot_sv_len_bar_chart(data, title, xlabel, ylabel, output_file, color, figsize=(6,5)):
    counts, edges = np.histogram(data, bins=LENGTH_BINS)
    fig, ax = plt.subplots(figsize=figsize)
    bars = ax.bar(BIN_LABELS, counts, color=color)
    ax.bar_label(bars, labels=[f'{v}' for v in counts], padding=3)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


def main():
    df_stixlrmr5 = pd.read_csv(args.stixlrmr5, sep='\t')
    df_stixlrmr1 = pd.read_csv(args.stixlrmr1, sep='\t')
    df_needlr = pd.read_csv(args.needlr, sep='\t')
    df_svafotate = pd.read_csv(args.svafotate, sep='\t')
    vcf = VCF(args.query_vcf)
    n = vcf.num_records

    if not args.cached_data:
        df_out = pd.DataFrame(columns=['svid', 'svtype', 'svlen', 'stixlr_mr1_samples', 'stixlr_mr5_samples', 'needlr_af', 'svafotate_af'])
        n = vcf.num_records

        for i,v in enumerate(vcf):
            if i % 100 == 0:
                print(f"Processing variant {i}/{n}")
            svid = v.ID
            svtype = v.INFO.get('SVTYPE')
            svlen = v.INFO.get('SVLEN')
            svlen = abs(svlen) if svlen is not None else None
            try:
                stixlr_mr1_samples = df_stixlrmr1.loc[df_stixlrmr1[STIX_SVID_COL] == svid, STIX_SAMPLE_COL].values[0]
            except IndexError:
                stixlr_mr1_samples = 0

            try:
                stixlr_mr5_samples = df_stixlrmr5.loc[df_stixlrmr5[STIX_SVID_COL] == svid, STIX_SAMPLE_COL].values[0]
            except IndexError:
                stixlr_mr5_samples = 0

            try:
                needlr_af = df_needlr.loc[df_needlr[NEEDLR_SVID_COL] == svid, NEEDLR_AF_COL].values[0]
            except IndexError:
                needlr_af = 0

            try:
                svafotate_af = df_svafotate.loc[df_svafotate[SVAFOTATE_SVID_COL] == svid, SVAFOTATE_AF_COL].values[0]
            except IndexError:
                svafotate_af = 0

            df_out = pd.concat([df_out, pd.DataFrame([{
                'svid': svid,
                'svtype': svtype,
                'svlen': svlen,
                'stixlr_mr1_samples': stixlr_mr1_samples,
                'stixlr_mr5_samples': stixlr_mr5_samples,
                'needlr_af': needlr_af,
                'svafotate_af': svafotate_af
            }])], ignore_index=True)
        df_out.to_csv(f"{args.out_prefix}-combined.tsv", sep='\t', index=False)
    else:
        df_out = pd.read_csv(args.cached_data, sep='\t')
    # type counts
    stixlr_mr1_type_counts_recovered = dict(df_out[df_out['stixlr_mr1_samples'] > 0]['svtype'].value_counts())
    stixlr_mr1_type_counts_missed = dict(df_out[df_out['stixlr_mr1_samples'] <= 0]['svtype'].value_counts())
    stixlr_mr5_type_counts_recovered = dict(df_out[df_out['stixlr_mr5_samples'] > 0]['svtype'].value_counts())
    stixlr_mr5_type_counts_missed = dict(df_out[df_out['stixlr_mr5_samples'] <= 0]['svtype'].value_counts())
    needlr_type_counts_recovered = dict(df_out[df_out['needlr_af'] > 0]['svtype'].value_counts())
    needlr_type_counts_missed = dict(df_out[df_out['needlr_af'] <= 0]['svtype'].value_counts())
    svafotate_type_counts_recovered = dict(df_out[df_out['svafotate_af'] > 0]['svtype'].value_counts())
    svafotate_type_counts_missed = dict(df_out[df_out['svafotate_af'] <= 0]['svtype'].value_counts())
    ### plot
    ## types
    plot_sv_type_bar_chart(
        stixlr_mr1_type_counts_recovered, f"{SVCALLSET} STIX-LR MR=1 recovered", XLABEL_TYPE_BAR, YLABEL_TYPE_BAR, f"{args.out_prefix}-stixlr_mr1-recovered-type-bar.png", color='blue', figsize=args.figsize)
    plot_sv_type_bar_chart(
        stixlr_mr1_type_counts_missed, f"{SVCALLSET} STIX-LR MR=1 missed", XLABEL_TYPE_BAR, YLABEL_TYPE_BAR, f"{args.out_prefix}-stixlr_mr1-missed-type-bar.png", color='red', figsize=args.figsize)
    plot_sv_type_bar_chart(
        stixlr_mr5_type_counts_recovered, f"{SVCALLSET} STIX-LR MR=5 recovered", XLABEL_TYPE_BAR, YLABEL_TYPE_BAR, f"{args.out_prefix}-stixlr_mr5-recovered-type-bar.png", color='blue', figsize=args.figsize)
    plot_sv_type_bar_chart(
        stixlr_mr5_type_counts_missed, f"{SVCALLSET} STIX-LR MR=5 missed", XLABEL_TYPE_BAR, YLABEL_TYPE_BAR, f"{args.out_prefix}-stixlr_mr5-missed-type-bar.png", color='red', figsize=args.figsize)
    plot_sv_type_bar_chart(
        needlr_type_counts_recovered, f"{SVCALLSET} needLR recovered", XLABEL_TYPE_BAR, YLABEL_TYPE_BAR, f"{args.out_prefix}-needlr-recovered-type-bar.png", color='blue', figsize=args.figsize)
    plot_sv_type_bar_chart(
        needlr_type_counts_missed, f"{SVCALLSET} needLR missed", XLABEL_TYPE_BAR, YLABEL_TYPE_BAR, f"{args.out_prefix}-needlr-missed-type-bar.png", color='red', figsize=args.figsize)
    plot_sv_type_bar_chart(
        svafotate_type_counts_recovered, f"{SVCALLSET} SVAFotate recovered", XLABEL_TYPE_BAR, YLABEL_TYPE_BAR, f"{args.out_prefix}-svafotate-recovered-type-bar.png", color='blue', figsize=args.figsize)
    plot_sv_type_bar_chart(
        svafotate_type_counts_missed, f"{SVCALLSET} SVAFotate missed", XLABEL_TYPE_BAR, YLABEL_TYPE_BAR, f"{args.out_prefix}-svafotate-missed-type-bar.png", color='red', figsize=args.figsize)
    ## lengths
    plot_sv_len_bar_chart(
        df_out[df_out['stixlr_mr1_samples'] > 0]['svlen'], f"{SVCALLSET} STIX-LR MR=1 recovered", XLABEL_LENGTH_BAR, YLABEL_LENGTH_BAR, f"{args.out_prefix}-stixlr_mr1-recovered-length-bar.png", color='blue', figsize=args.figsize)
    plot_sv_len_bar_chart(
        df_out[df_out['stixlr_mr1_samples'] <= 0]['svlen'], f"{SVCALLSET} STIX-LR MR=1 missed", XLABEL_LENGTH_BAR, YLABEL_LENGTH_BAR, f"{args.out_prefix}-stixlr_mr1-missed-length-bar.png", color='red', figsize=args.figsize)
    plot_sv_len_bar_chart(
        df_out[df_out['stixlr_mr5_samples'] > 0]['svlen'], f"{SVCALLSET} STIX-LR MR=5 recovered", XLABEL_LENGTH_BAR, YLABEL_LENGTH_BAR, f"{args.out_prefix}-stixlr_mr5-recovered-length-bar.png", color='blue', figsize=args.figsize)
    plot_sv_len_bar_chart(
        df_out[df_out['stixlr_mr5_samples'] <= 0]['svlen'], f"{SVCALLSET} STIX-LR MR=5 missed", XLABEL_LENGTH_BAR, YLABEL_LENGTH_BAR, f"{args.out_prefix}-stixlr_mr5-missed-length-bar.png", color='red', figsize=args.figsize)
    plot_sv_len_bar_chart(
        df_out[df_out['needlr_af'] > 0]['svlen'], f"{SVCALLSET} needLR recovered", XLABEL_LENGTH_BAR, YLABEL_LENGTH_BAR, f"{args.out_prefix}-needlr-recovered-length-bar.png", color='blue', figsize=args.figsize)
    plot_sv_len_bar_chart(
        df_out[df_out['needlr_af'] <= 0]['svlen'], f"{SVCALLSET} needLR missed", XLABEL_LENGTH_BAR, YLABEL_LENGTH_BAR, f"{args.out_prefix}-needlr-missed-length-bar.png", color='red', figsize=args.figsize)
    plot_sv_len_bar_chart(
        df_out[df_out['svafotate_af'] > 0]['svlen'], f"{SVCALLSET} SVAFotate recovered", XLABEL_LENGTH_BAR, YLABEL_LENGTH_BAR, f"{args.out_prefix}-svafotate-recovered-length-bar.png", color='blue', figsize=args.figsize)
    plot_sv_len_bar_chart(
        df_out[df_out['svafotate_af'] <= 0]['svlen'], f"{SVCALLSET} SVAFotate missed", XLABEL_LENGTH_BAR, YLABEL_LENGTH_BAR, f"{args.out_prefix}-svafotate-missed-length-bar.png", color='red', figsize=args.figsize)
    ### recall
    with open(f"{args.out_prefix}-recall.tsv", 'w') as f:
        f.write("Method\trecall\n")
        stixlr_mr1_recall = len(df_out[df_out['stixlr_mr1_samples'] > 0]) / len(df_out)
        stixlr_mr5_recall = len(df_out[df_out['stixlr_mr5_samples'] > 0]) / len(df_out)
        needlr_recall = len(df_out[df_out['needlr_af'] > 0]) / len(df_out)
        svafotate_recall = len(df_out[df_out['svafotate_af'] > 0]) / len(df_out)
        f.write(f"STIX-LR MR=1\t{stixlr_mr1_recall:.4f}\n")
        f.write(f"STIX-LR MR=5\t{stixlr_mr5_recall:.4f}\n")
        f.write(f"needLR\t{needlr_recall:.4f}\n")
        f.write(f"SVAFotate\t{svafotate_recall:.4f}\n")
    ### type miss fraction
    needlr_frac_del_missed = 0
    needlr_frac_ins_missed = 0
    stixlr_mr1_frac_del_missed = 0
    stixlr_mr1_frac_ins_missed = 0
    stixlr_mr5_frac_del_missed = 0
    stixlr_mr5_frac_ins_missed = 0
    svafotate_frac_del_missed = 0
    svafotate_frac_ins_missed = 0
    # needlr
    if 'DEL' in needlr_type_counts_missed.keys():
        needlr_total_del = needlr_type_counts_missed['DEL'] + needlr_type_counts_recovered['DEL']
        needlr_frac_del_missed = needlr_type_counts_missed['DEL'] / needlr_total_del
    if 'INS' in needlr_type_counts_missed.keys():
        needlr_total_ins = needlr_type_counts_missed['INS'] + needlr_type_counts_recovered['INS']
        needlr_frac_ins_missed = needlr_type_counts_missed['INS'] / needlr_total_ins
    # stixlr mr1
    if 'DEL' in stixlr_mr1_type_counts_missed.keys():
        stixlr_mr1_total_del = stixlr_mr1_type_counts_missed['DEL'] + stixlr_mr1_type_counts_recovered['DEL']
        stixlr_mr1_frac_del_missed = stixlr_mr1_type_counts_missed['DEL'] / stixlr_mr1_total_del
    if 'INS' in stixlr_mr1_type_counts_missed.keys():
        stixlr_mr1_total_ins = stixlr_mr1_type_counts_missed['INS'] + stixlr_mr1_type_counts_recovered['INS']
        stixlr_mr1_frac_ins_missed = stixlr_mr1_type_counts_missed['INS'] / stixlr_mr1_total_ins
    # stixlr mr5
    if 'DEL' in stixlr_mr5_type_counts_missed.keys():
        stixlr_mr5_total_del = stixlr_mr5_type_counts_missed['DEL'] + stixlr_mr5_type_counts_recovered['DEL']
        stixlr_mr5_frac_del_missed = stixlr_mr5_type_counts_missed['DEL'] / stixlr_mr5_total_del
    if 'INS' in stixlr_mr5_type_counts_missed.keys():
        stixlr_mr5_total_ins = stixlr_mr5_type_counts_missed['INS'] + stixlr_mr5_type_counts_recovered['INS']
        stixlr_mr5_frac_ins_missed = stixlr_mr5_type_counts_missed['INS'] / stixlr_mr5_total_ins
    # svafotate
    if 'DEL' in svafotate_type_counts_missed.keys():
        svafotate_total_del = svafotate_type_counts_missed['DEL'] + svafotate_type_counts_recovered['DEL']
        svafotate_frac_del_missed = svafotate_type_counts_missed['DEL'] / svafotate_total_del
    if 'INS' in svafotate_type_counts_missed.keys():
        svafotate_total_ins = svafotate_type_counts_missed['INS'] + svafotate_type_counts_recovered['INS']
        svafotate_frac_ins_missed = svafotate_type_counts_missed['INS'] / svafotate_total_ins
    with open(f"{args.out_prefix}-type-miss-fractions.tsv", "w") as f:
        f.write("method\tfraction_del_missed\tfraction_ins_missed\n")
        f.write(f"STIX-LR MR=1\t{stixlr_mr1_frac_del_missed}\t{stixlr_mr1_frac_ins_missed}\n")
        f.write(f"STIX-LR MR=5\t{stixlr_mr5_frac_del_missed}\t{stixlr_mr5_frac_ins_missed}\n")
        f.write(f"needLR\t{needlr_frac_del_missed}\t{needlr_frac_ins_missed}\n")
        f.write(f"SVAFotate\t{svafotate_frac_del_missed}\t{svafotate_frac_ins_missed}\n")




if __name__ == "__main__":
    main()