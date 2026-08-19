#!/usr/bin/env python3

import argparse
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from cyvcf2 import VCF

parser = argparse.ArgumentParser(description='SV frequency benchmark summary')
# vcfs
parser.add_argument('--vcf_hg002', default='../../data/2026_07-hg002-svs/GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.AF.addEND.gt50bp.vcf.gz')
parser.add_argument('--vcf_hg002_cmrg', default='../../data/2025_12-hg002-cmrg/HG002_GRCh38_difficult_medical_gene_SV_benchmark_v0.01_trusted_SVTYPE.addID.svafotate.AF.addEND.vcf.gz')
parser.add_argument('--vcf_cosmic', default='../2026_01-cosmic-tsv-to-vcf/cosmic.v103.grch38.vcf.gz')
parser.add_argument('--vcf_thousg', default='../../data/2026_08-thousg_svs/1KGP.subset.vcf.gz')
parser.add_argument('--vcf_colo_germline', default='../2025_12-colo-filtered/colo829_germline.vcf')
parser.add_argument('--vcf_colo_somatic', default='../2025_12-colo-filtered/colo829_somatic_grch38_nogt00.vcf')
# stixlr
parser.add_argument('--stix_samples', default=1108)
parser.add_argument('--stixlr_hg002_mr1', default='../2026_08-hg002-stix_lr/hg002-stix_lr-min_read_1.popfreq.tsv')
parser.add_argument('--stixlr_hg002_mr5', default='../2026_08-hg002-stix_lr/hg002-stix_lr-min_read_5.popfreq.tsv')
parser.add_argument('--stixlr_hg002_cmrg_mr1', default='../2025_12-hg002_cmrg-stix_lr/hg002_cmrg.stix_lr.min_read_1.popfreq.tsv')
parser.add_argument('--stixlr_hg002_cmrg_mr5', default='../2025_12-hg002_cmrg-stix_lr/hg002_cmrg.stix_lr.min_read_5.popfreq.tsv')
parser.add_argument('--stixlr_cosmic_mr1', default='../2026_01-cosmic-stix_lr/cosmic.stix_lr.min_read_1.tsv')
parser.add_argument('--stixlr_cosmic_mr5', default='../2026_01-cosmic-stix_lr/cosmic.stix_lr.min_read_5.tsv')
parser.add_argument('--stixlr_thousg_mr1', default='../2026_08-1kg-stixlr/onekg-stix_lr-min_read_1.popfreq.tsv')
parser.add_argument('--stixlr_thousg_mr5', default='../2026_08-1kg-stixlr/onekg-stix_lr-min_read_5.popfreq.tsv')
parser.add_argument('--stixlr_colo_germline_mr1', default = '../2026_01-colo_filt-stix_lr-rerun/colo_germline-stix_lr-min_read_1.popfreq.tsv')
parser.add_argument('--stixlr_colo_germline_mr5', default = '../2026_01-colo_filt-stix_lr-rerun/colo_germline-stix_lr-min_read_5.popfreq.tsv')
parser.add_argument('--stixlr_colo_somatic_mr1', default = '../2026_01-colo_filt-stix_lr-rerun/colo_somatic-stix_lr-min_read_1.popfreq.tsv')
parser.add_argument('--stixlr_colo_somatic_mr5', default = '../2026_01-colo_filt-stix_lr-rerun/colo_somatic-stix_lr-min_read_5.popfreq.tsv')
# svafotate
parser.add_argument('--svafotate_hg002_ov05', default='../2026_08-hg002-svafotate/svafotate-hg002_overlap_0.5_maxpopfreq.txt')
parser.add_argument('--svafotate_hg002_ov07', default='../2026_08-hg002-svafotate/svafotate-hg002_overlap_0.7_maxpopfreq.txt')
parser.add_argument('--svafotate_hg002_ov09', default='../2026_08-hg002-svafotate/svafotate-hg002_overlap_0.9_maxpopfreq.txt')
parser.add_argument('--svafotate_hg002_cmrg_ov05', default='../2025_12-hg002_cmrg-svafotate/svafotate-hg002-cmrg-overlap_0.5_maxpopfreq.txt')
parser.add_argument('--svafotate_hg002_cmrg_ov07', default='../2025_12-hg002_cmrg-svafotate/svafotate-hg002-cmrg-overlap_0.7_maxpopfreq.txt')
parser.add_argument('--svafotate_hg002_cmrg_ov09', default='../2025_12-hg002_cmrg-svafotate/svafotate-hg002-cmrg-overlap_0.9_maxpopfreq.txt')
parser.add_argument('--svafotate_cosmic_ov05', default = '../2026_01-cosmic-svafotate/svafotate-cosmic_overlap_0.5_maxpopfreq.txt')
parser.add_argument('--svafotate_cosmic_ov07', default = '../2026_01-cosmic-svafotate/svafotate-cosmic_overlap_0.7_maxpopfreq.txt')
parser.add_argument('--svafotate_cosmic_ov09', default = '../2026_01-cosmic-svafotate/svafotate-cosmic_overlap_0.9_maxpopfreq.txt')
parser.add_argument('--svafotate_thousg_ov05', default = '../2026_08-1kg-svafotate/svafotate-1kg_overlap_0.5_maxpopfreq.txt')
parser.add_argument('--svafotate_thousg_ov07', default = '../2026_08-1kg-svafotate/svafotate-1kg_overlap_0.7_maxpopfreq.txt')
parser.add_argument('--svafotate_thousg_ov09', default = '../2026_08-1kg-svafotate/svafotate-1kg_overlap_0.9_maxpopfreq.txt')
parser.add_argument('--svafotate_colo_germline_ov05', default='../2025_12-colo-svafotate-filtered/svafotate.colo_germline.svid_popfreq.ov0.5.txt')
parser.add_argument('--svafotate_colo_germline_ov07', default='../2025_12-colo-svafotate-filtered/svafotate.colo_germline.svid_popfreq.ov0.7.txt')
parser.add_argument('--svafotate_colo_germline_ov09', default='../2025_12-colo-svafotate-filtered/svafotate.colo_germline.svid_popfreq.ov0.9.txt')
parser.add_argument('--svafotate_colo_somatic_ov05', default='../2025_12-colo-svafotate-filtered/svafotate.colo_somatic.svid_popfreq.ov0.5.txt')
parser.add_argument('--svafotate_colo_somatic_ov07', default='../2025_12-colo-svafotate-filtered/svafotate.colo_somatic.svid_popfreq.ov0.7.txt')
parser.add_argument('--svafotate_colo_somatic_ov09', default='../2025_12-colo-svafotate-filtered/svafotate.colo_somatic.svid_popfreq.ov0.9.txt')
# needlr
parser.add_argument('--needlr_hg002_ov05', default = '../2026_07-hg002-needlr/needLR_ov0.5/needlr_pop_freq.tsv')
parser.add_argument('--needlr_hg002_ov07', default = '../2026_07-hg002-needlr/needLR_ov0.7/needlr_pop_freq.tsv')
parser.add_argument('--needlr_hg002_ov09', default = '../2026_07-hg002-needlr/needLR_ov0.9/needlr_pop_freq.tsv')
parser.add_argument('--needlr_hg002_cmrg_ov05', default = '../2026_07-hg002_cmrg-needlr/needLR_ov0.5/needlr_pop_freq.tsv')
parser.add_argument('--needlr_hg002_cmrg_ov07', default = '../2026_07-hg002_cmrg-needlr/needLR_ov0.7/needlr_pop_freq.tsv')
parser.add_argument('--needlr_hg002_cmrg_ov09', default = '../2026_07-hg002_cmrg-needlr/needLR_ov0.9/needlr_pop_freq.tsv')
parser.add_argument('--needlr_cosmic_ov05', default='../2026_08-cosmic-needlr/needLR_ov0.5/needlr_pop_freq.tsv')
parser.add_argument('--needlr_cosmic_ov07', default='../2026_08-cosmic-needlr/needLR_ov0.7/needlr_pop_freq.tsv')
parser.add_argument('--needlr_cosmic_ov09', default='../2026_08-cosmic-needlr/needLR_ov0.9/needlr_pop_freq.tsv')
parser.add_argument('--needlr_thousg_ov05', default='../2026_08-1kg-needlr/needLR_ov0.5/needlr_pop_freq.tsv')
parser.add_argument('--needlr_thousg_ov07', default='../2026_08-1kg-needlr/needLR_ov0.7/needlr_pop_freq.tsv')
parser.add_argument('--needlr_thousg_ov09', default='../2026_08-1kg-needlr/needLR_ov0.9/needlr_pop_freq.tsv')
parser.add_argument('--needlr_colo_germline_ov05', default= '../2026_07-colo-needlr/germline_needLR_ov0.5/needlr_pop_freq.tsv')
parser.add_argument('--needlr_colo_germline_ov07', default= '../2026_07-colo-needlr/germline_needLR_ov0.7/needlr_pop_freq.tsv')
parser.add_argument('--needlr_colo_germline_ov09', default= '../2026_07-colo-needlr/germline_needLR_ov0.9/needlr_pop_freq.tsv')
parser.add_argument('--needlr_colo_somatic_ov05', default= '../2026_07-colo-needlr/somatic_needLR_ov0.5/needlr_pop_freq.tsv')
parser.add_argument('--needlr_colo_somatic_ov07', default= '../2026_07-colo-needlr/somatic_needLR_ov0.7/needlr_pop_freq.tsv')
parser.add_argument('--needlr_colo_somatic_ov09', default= '../2026_07-colo-needlr/somatic_needLR_ov0.9/needlr_pop_freq.tsv')
args = parser.parse_args()

# 0-indexed
COL_IDX_STIXLR_SAMPLES=1
COL_IDX_SVAFOTATE_AF=1
COL_IDX_NEEDLR_AF=2
COL_NAME_SVID='svid'
COL_NAME_STIXLR_SAMPLES='stix_samples'
COL_NAME_SVAFOTATE_AF='svafotate_af'
COL_NAME_NEEDLR_AF='needlr_af'

def bin_frequencies(frequencies):
    counts = pd.Series({
    "[0,0]": (frequencies == 0).sum(),
    "(0,0.001]": ((frequencies > 0) & (frequencies <= 0.001)).sum(),
    "(0.001,0.75]": ((frequencies > 0.001) & (frequencies <= 0.75)).sum(),
    "(0.75,1]": ((frequencies > 0.75) & (frequencies <= 1)).sum(),
    })
    return counts

def plot_frequency_bins(datasets):
    for name, df in datasets.items():
        frequency_cols = [c for c in df.columns if c != COL_NAME_SVID]

        counts = pd.DataFrame({
            col: bin_frequencies(df[col])
            for col in frequency_cols
        })

        ax = counts.plot.bar()
        ax.set_title(name, loc='left', fontsize=10)
        ax.set_xlabel("Population/Allele frequency")
        ax.set_ylabel("SV count")
        ax.legend(fontsize=7)

        # for container in ax.containers:
        #     ax.bar_label(container, fmt='%d', padding=2, fontsize=8)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        l1 = plt.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0)
        plt.subplots_adjust(right=0.7)
        plt.savefig(f"{name.lower().replace(' ', '_')}-freq_bin.png")

def plot_recall_bar(df_recall, name):
    fig, ax = plt.subplots()
    ax.bar(df_recall['tool'], df_recall['recall'])
    for container in ax.containers:
        ax.bar_label(container, fmt='%.4f', padding=2, fontsize=8)
    ax.set_xlabel("Tool")
    ax.set_ylabel("Recall")
    ax.set_title(name, loc='left', fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.tight_layout()
    plt.savefig(f"{name.lower().replace(' ', '_')}-recall.png")

def normalize_stix(x, denom=args.stix_samples):
    return x / args.stix_samples

def merged2recall(df_merge):
    # make a dataframe of svids for key
    cols = df_merge.columns
    recalls={}
    m = df_merge.shape[0]
    for col in cols:
        if col != COL_NAME_SVID:
            mask = df_merge[col] > 0
            recall = mask.sum() / m
            recalls[col]=recall
    recalls = pd.DataFrame(list(recalls.items()), columns = ['tool', 'recall'])
    return recalls

def merge_dfs(dfs, svids,fillna=0):
    df_svid = pd.DataFrame({COL_NAME_SVID: list(svids)})
    dfs = [df_svid] + dfs
    merged = reduce(
        lambda left, right: left.merge(right, on=COL_NAME_SVID, how="outer"),
        dfs
    )
    merged.fillna(fillna, inplace=True)
    return merged

def vcf2ids(path_vcf):
    vcf = VCF(path_vcf)
    ids = set()
    for v in vcf:
        ids.add(v.ID)
    return ids


def main():
    merged_datasets={}
    ### hg002
    ids_hg002 = vcf2ids(args.vcf_hg002)
    df_hg002_stixlrmr1 = pd.read_csv(args.stixlr_hg002_mr1, sep='\t')
    df_hg002_stixlrmr1.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr1']
    df_hg002_stixlrmr1[COL_NAME_STIXLR_SAMPLES + '_mr1'] = df_hg002_stixlrmr1[COL_NAME_STIXLR_SAMPLES + '_mr1'].apply(normalize_stix)
    df_hg002_stixlrmr5 = pd.read_csv(args.stixlr_hg002_mr5, sep='\t')
    df_hg002_stixlrmr5.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr5']
    df_hg002_stixlrmr5[COL_NAME_STIXLR_SAMPLES + '_mr5'] = df_hg002_stixlrmr5[COL_NAME_STIXLR_SAMPLES + '_mr5'].apply(normalize_stix)
    df_hg002_svafotate05 = pd.read_csv(args.svafotate_hg002_ov05, sep='\t')
    df_hg002_svafotate05.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov05']
    df_hg002_svafotate07 = pd.read_csv(args.svafotate_hg002_ov07, sep='\t')
    df_hg002_svafotate07.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov07']
    df_hg002_svafotate09 = pd.read_csv(args.svafotate_hg002_ov09, sep='\t')
    df_hg002_svafotate09.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov09']
    df_hg002_needlr05 = pd.read_csv(args.needlr_hg002_ov05, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_hg002_needlr05.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov05']
    df_hg002_needlr07 = pd.read_csv(args.needlr_hg002_ov07, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_hg002_needlr07.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov07']
    df_hg002_needlr09 = pd.read_csv(args.needlr_hg002_ov09, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_hg002_needlr09.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov09']
    dfs2merge = [
            df_hg002_stixlrmr1,
            df_hg002_stixlrmr5,
            df_hg002_svafotate05,
            df_hg002_svafotate07,
            df_hg002_svafotate09,
            df_hg002_needlr05,
            df_hg002_needlr07,
            df_hg002_needlr09
    ]
    print("# merging hg002")
    df_merged = merge_dfs(dfs2merge, ids_hg002)
    df_merged.to_csv('hg002-merge.tsv', sep='\t', index=False)
    name = "HG002 SVs"
    merged_datasets[name] = df_merged
    df_recall = merged2recall(df_merged)
    plot_recall_bar(df_recall, name)
    df_recall.to_csv('hg002-recall.tsv',sep='\t', index=False)
    ### hg002 cmrg
    ids_hg002cmrg = vcf2ids(args.vcf_hg002_cmrg)
    df_hg002cmrg_stixlrmr1 = pd.read_csv(args.stixlr_hg002_cmrg_mr1, sep='\t')
    df_hg002cmrg_stixlrmr1.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr1']
    df_hg002cmrg_stixlrmr1[COL_NAME_STIXLR_SAMPLES + '_mr1'] = df_hg002cmrg_stixlrmr1[COL_NAME_STIXLR_SAMPLES + '_mr1'].apply(normalize_stix)
    df_hg002cmrg_stixlrmr5 = pd.read_csv(args.stixlr_hg002_cmrg_mr5, sep='\t')
    df_hg002cmrg_stixlrmr5.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr5']
    df_hg002cmrg_stixlrmr5[COL_NAME_STIXLR_SAMPLES + '_mr5'] = df_hg002cmrg_stixlrmr5[COL_NAME_STIXLR_SAMPLES + '_mr5'].apply(normalize_stix)
    df_hg002cmrg_svafotate05 = pd.read_csv(args.svafotate_hg002_cmrg_ov05, sep='\t')
    df_hg002cmrg_svafotate05.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov05']
    df_hg002cmrg_svafotate07 = pd.read_csv(args.svafotate_hg002_cmrg_ov07, sep='\t')
    df_hg002cmrg_svafotate07.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov07']
    df_hg002cmrg_svafotate09 = pd.read_csv(args.svafotate_hg002_cmrg_ov09, sep='\t')
    df_hg002cmrg_svafotate09.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov09']
    df_hg002cmrg_needlr05 = pd.read_csv(args.needlr_hg002_cmrg_ov05, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_hg002cmrg_needlr05.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov05']
    df_hg002cmrg_needlr07 = pd.read_csv(args.needlr_hg002_cmrg_ov07, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_hg002cmrg_needlr07.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov07']
    df_hg002cmrg_needlr09 = pd.read_csv(args.needlr_hg002_cmrg_ov09, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_hg002cmrg_needlr09.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov09']
    dfs2merge = [
            df_hg002cmrg_stixlrmr1,
            df_hg002cmrg_stixlrmr5,
            df_hg002cmrg_svafotate05,
            df_hg002cmrg_svafotate07,
            df_hg002cmrg_svafotate09,
            df_hg002cmrg_needlr05,
            df_hg002cmrg_needlr07,
            df_hg002cmrg_needlr09
    ]
    print("# merging hg002cmrg")
    df_merge = merge_dfs(dfs2merge, ids_hg002cmrg)
    df_merge.to_csv('hg002cmrg-merge.tsv', sep='\t', index=False)
    name = "HG002 CMRG SVs"
    merged_datasets[name] = df_merge
    df_recall = merged2recall(df_merge)
    plot_recall_bar(df_recall, name)
    df_recall.to_csv('hg002_cmrg-recall.tsv',sep='\t', index=False)
    ### cosmic
    ids_cosmic = vcf2ids(args.vcf_cosmic)
    df_cosmic_stixlrmr1 = pd.read_csv(args.stixlr_cosmic_mr1, sep='\t')
    df_cosmic_stixlrmr1.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr1']
    df_cosmic_stixlrmr1[COL_NAME_STIXLR_SAMPLES + '_mr1'] = df_cosmic_stixlrmr1[COL_NAME_STIXLR_SAMPLES + '_mr1'].apply(normalize_stix)
    df_cosmic_stixlrmr5 = pd.read_csv(args.stixlr_cosmic_mr5, sep='\t')
    df_cosmic_stixlrmr5.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr5']
    df_cosmic_stixlrmr5[COL_NAME_STIXLR_SAMPLES + '_mr5'] = df_cosmic_stixlrmr5[COL_NAME_STIXLR_SAMPLES + '_mr5'].apply(normalize_stix)
    df_cosmic_svafotate05 = pd.read_csv(args.svafotate_cosmic_ov05, sep='\t')
    df_cosmic_svafotate05.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov05']
    df_cosmic_svafotate07 = pd.read_csv(args.svafotate_cosmic_ov07, sep='\t')
    df_cosmic_svafotate07.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov07']
    df_cosmic_svafotate09 = pd.read_csv(args.svafotate_cosmic_ov09, sep='\t')
    df_cosmic_svafotate09.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov09']
    df_cosmic_needlr05 = pd.read_csv(args.needlr_cosmic_ov05, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_cosmic_needlr05.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov05']
    df_cosmic_needlr07 = pd.read_csv(args.needlr_cosmic_ov07, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_cosmic_needlr07.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov07']
    df_cosmic_needlr09 = pd.read_csv(args.needlr_cosmic_ov09, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_cosmic_needlr09.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov09']
    dfs2merge = [
            df_cosmic_stixlrmr1,
            df_cosmic_stixlrmr5,
            df_cosmic_svafotate05,
            df_cosmic_svafotate07,
            df_cosmic_svafotate09,
            df_cosmic_needlr05,
            df_cosmic_needlr07,
            df_cosmic_needlr09
    ]
    print("# merging cosmic")
    df_merge = merge_dfs(dfs2merge, ids_cosmic)
    df_merge.to_csv('cosmic-merge.tsv', sep='\t', index=False)
    name = "COSMIC"
    merged_datasets[name] = df_merge
    df_recall = merged2recall(df_merge)
    plot_recall_bar(df_recall, name)
    df_recall.to_csv('cosmic-recall.tsv',sep='\t', index=False)
    ### 1000G
    ids_thousg = vcf2ids(args.vcf_thousg)
    df_thousg_stixlrmr1 = pd.read_csv(args.stixlr_thousg_mr1, sep='\t')
    df_thousg_stixlrmr1.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr1']
    df_thousg_stixlrmr1[COL_NAME_STIXLR_SAMPLES + '_mr1'] = df_thousg_stixlrmr1[COL_NAME_STIXLR_SAMPLES + '_mr1'].apply(normalize_stix)
    df_thousg_stixlrmr5 = pd.read_csv(args.stixlr_thousg_mr5, sep='\t')
    df_thousg_stixlrmr5.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr5']
    df_thousg_stixlrmr5[COL_NAME_STIXLR_SAMPLES + '_mr5'] = df_thousg_stixlrmr5[COL_NAME_STIXLR_SAMPLES + '_mr5'].apply(normalize_stix)
    df_thousg_svafotate05 = pd.read_csv(args.svafotate_thousg_ov05, sep='\t')
    df_thousg_svafotate05.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov05']
    df_thousg_svafotate07 = pd.read_csv(args.svafotate_thousg_ov07, sep='\t')
    df_thousg_svafotate07.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov07']
    df_thousg_svafotate09 = pd.read_csv(args.svafotate_thousg_ov09, sep='\t')
    df_thousg_svafotate09.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov09']
    df_thousg_needlr05 = pd.read_csv(args.needlr_thousg_ov05, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_thousg_needlr05.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov05']
    df_thousg_needlr07 = pd.read_csv(args.needlr_thousg_ov07, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_thousg_needlr07.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov07']
    df_thousg_needlr09 = pd.read_csv(args.needlr_thousg_ov09, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_thousg_needlr09.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov09']
    dfs2merge = [
            df_thousg_stixlrmr1,
            df_thousg_stixlrmr5,
            df_thousg_svafotate05,
            df_thousg_svafotate07,
            df_thousg_svafotate09,
            df_thousg_needlr05,
            df_thousg_needlr07,
            df_thousg_needlr09
    ]
    print("# merging 1000G")
    df_merge = merge_dfs(dfs2merge, vcf2ids(args.vcf_thousg))
    df_merge.to_csv('thousg-merge.tsv', sep='\t', index=False)
    name = "1kg SVs"
    merged_datasets[name] = df_merge
    df_recall = merged2recall(df_merge)
    plot_recall_bar(df_recall, name)
    df_recall.to_csv('thousg-recall.tsv',sep='\t', index=False)
    ### colo germline
    ids_colo_germline = vcf2ids(args.vcf_colo_germline)
    df_colo_germline_stixlrmr1 = pd.read_csv(args.stixlr_colo_germline_mr1, sep='\t')
    df_colo_germline_stixlrmr1.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr1']
    df_colo_germline_stixlrmr1[COL_NAME_STIXLR_SAMPLES + '_mr1'] = df_colo_germline_stixlrmr1[COL_NAME_STIXLR_SAMPLES + '_mr1'].apply(normalize_stix)
    df_colo_germline_stixlrmr5 = pd.read_csv(args.stixlr_colo_germline_mr5, sep='\t')
    df_colo_germline_stixlrmr5.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr5']
    df_colo_germline_stixlrmr5[COL_NAME_STIXLR_SAMPLES + '_mr5'] = df_colo_germline_stixlrmr5[COL_NAME_STIXLR_SAMPLES + '_mr5'].apply(normalize_stix)
    df_colo_germline_svafotate05 = pd.read_csv(args.svafotate_colo_germline_ov05, sep='\t')
    df_colo_germline_svafotate05.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov05']
    df_colo_germline_svafotate07 = pd.read_csv(args.svafotate_colo_germline_ov07, sep='\t')
    df_colo_germline_svafotate07.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov07']
    df_colo_germline_svafotate09 = pd.read_csv(args.svafotate_colo_germline_ov09, sep='\t')
    df_colo_germline_svafotate09.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov09']
    df_colo_germline_needlr05 = pd.read_csv(args.needlr_colo_germline_ov05, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_colo_germline_needlr05.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov05']
    df_colo_germline_needlr07 = pd.read_csv(args.needlr_colo_germline_ov07, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_colo_germline_needlr07.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov07']
    df_colo_germline_needlr09 = pd.read_csv(args.needlr_colo_germline_ov09, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_colo_germline_needlr09.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov09']
    dfs2merge = [
            df_colo_germline_stixlrmr1,
            df_colo_germline_stixlrmr5,
            df_colo_germline_svafotate05,
            df_colo_germline_svafotate07,
            df_colo_germline_svafotate09,
            df_colo_germline_needlr05,
            df_colo_germline_needlr07,
            df_colo_germline_needlr09
    ]
    print("# merging colo germline")
    df_merge = merge_dfs(dfs2merge, ids_colo_germline)
    name="COLO germline SVs"
    df_merge.to_csv('colo_germline-merge.tsv', sep='\t', index=False)
    merged_datasets[name] = df_merge
    df_recall = merged2recall(df_merge)
    plot_recall_bar(df_recall, name)
    df_recall.to_csv('colo_germline-recall.tsv',sep='\t', index=False)
    ### colo somatic
    ids_colo_somatic = vcf2ids(args.vcf_colo_somatic)
    df_colo_somatic_stixlrmr1 = pd.read_csv(args.stixlr_colo_somatic_mr1, sep='\t')
    df_colo_somatic_stixlrmr1.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr1']
    df_colo_somatic_stixlrmr1[COL_NAME_STIXLR_SAMPLES + '_mr1'] = df_colo_somatic_stixlrmr1[COL_NAME_STIXLR_SAMPLES + '_mr1'].apply(normalize_stix)
    df_colo_somatic_stixlrmr5 = pd.read_csv(args.stixlr_colo_somatic_mr5, sep='\t')
    df_colo_somatic_stixlrmr5.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr5']
    df_colo_somatic_stixlrmr5[COL_NAME_STIXLR_SAMPLES + '_mr5'] = df_colo_somatic_stixlrmr5[COL_NAME_STIXLR_SAMPLES + '_mr5'].apply(normalize_stix)
    df_colo_somatic_svafotate05 = pd.read_csv(args.svafotate_colo_somatic_ov05, sep='\t')
    df_colo_somatic_svafotate05.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov05']
    df_colo_somatic_svafotate07 = pd.read_csv(args.svafotate_colo_somatic_ov07, sep='\t')
    df_colo_somatic_svafotate07.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov07']
    df_colo_somatic_svafotate09 = pd.read_csv(args.svafotate_colo_somatic_ov09, sep='\t')
    df_colo_somatic_svafotate09.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov09']
    df_colo_somatic_needlr05 = pd.read_csv(args.needlr_colo_somatic_ov05, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_colo_somatic_needlr05.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov05']
    df_colo_somatic_needlr07 = pd.read_csv(args.needlr_colo_somatic_ov07, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_colo_somatic_needlr07.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov07']
    df_colo_somatic_needlr09 = pd.read_csv(args.needlr_colo_somatic_ov09, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_colo_somatic_needlr09.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov09']
    dfs2merge = [
            df_colo_somatic_stixlrmr1,
            df_colo_somatic_stixlrmr5,
            df_colo_somatic_svafotate05,
            df_colo_somatic_svafotate07,
            df_colo_somatic_svafotate09,
            df_colo_somatic_needlr05,
            df_colo_somatic_needlr07,
            df_colo_somatic_needlr09
    ]
    print("# merging colo somatic")
    df_merge = merge_dfs(dfs2merge, ids_colo_somatic)
    name = "COLO somatic SVs"
    df_merge.to_csv('colo_somatic-merge.tsv', sep='\t', index=False)
    merged_datasets[name] = df_merge
    df_recall = merged2recall(df_merge)
    plot_recall_bar(df_recall, name)
    df_recall.to_csv('colo_somatic-recall.tsv',sep='\t', index=False)
    plot_frequency_bins(merged_datasets)





    

if __name__ == "__main__":
    main()
