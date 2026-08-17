#!/usr/bin/env python3

import argparse
import pandas as pd
import os
from functools import reduce

parser = argparse.ArgumentParser(description='SV frequency benchmark summary')
# parser.add_argument('--stixlr_hg002_mr1', default='../2026_08-hg002-stix_lr/hg002-stix_lr-min_read_1.vcf')
# parser.add_argument('--stixlr_hg002_mr5', default='../2026_08-hg002-stix_lr/hg002-stix_lr-min_read_5.vcf')
# stixlr
parser.add_argument('--stix_samples', default=1108)
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
# did not run svafotate 1kg myself, but results are available at github.com/ryanlayer/lr_stix_analysis
# parser.add_argument('--svafotate_thousg_ov05', default = 
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

def main():
    ### hg002
    # df_stixlrmr1_hg002 = 
    # df_stixlrmr5_hg002 = 
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
            df_hg002_svafotate05,
            df_hg002_svafotate07,
            df_hg002_svafotate09,
            df_hg002_needlr05,
            df_hg002_needlr07,
            df_hg002_needlr09
    ]
    print("# merging hg002")
    merged = reduce(
        lambda left, right: left.merge(right, on=COL_NAME_SVID, how="inner"),
        dfs2merge
    )
    merged.to_csv('hg002-merge.tsv', sep='\t')
    ### hg002 cmrg
    print("# merging hg002cmrg")
    df_hg002cmrg_stixlrmr1 = pd.read_csv(args.stixlr_hg002_cmrg_mr1, sep='\t')
    df_hg002cmrg_stixlrmr1.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr1']
    df_hg002cmrg_stixlrmr5 = pd.read_csv(args.stixlr_hg002_cmrg_mr5, sep='\t')
    df_hg002cmrg_stixlrmr5.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr5']
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
    merged = reduce(
        lambda left, right: left.merge(right, on=COL_NAME_SVID, how="inner"),
        dfs2merge
    )
    merged.to_csv('hg002cmrg-merge.tsv', sep='\t')
    ### cosmic
    df_cosmic_stixlrmr1 = pd.read_csv(args.stixlr_cosmic_mr1, sep='\t')
    df_cosmic_stixlrmr1.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr1']
    df_cosmic_stixlrmr5 = pd.read_csv(args.stixlr_cosmic_mr5, sep='\t')
    df_cosmic_stixlrmr5.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr5']
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
    merged = reduce(
        lambda left, right: left.merge(right, on=COL_NAME_SVID, how="inner"),
        dfs2merge
    )
    merged.to_csv('cosmic-merge.tsv', sep='\t')
    ### 1000G
    df_thousg_stixlrmr1 = pd.read_csv(args.stixlr_thousg_mr1, sep='\t')
    df_thousg_stixlrmr1.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr1']
    df_thousg_stixlrmr5 = pd.read_csv(args.stixlr_thousg_mr5, sep='\t')
    df_thousg_stixlrmr5.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr5']
    # df_thousg_svafotate05 = pd.read_csv(args.svafotate_thousg_ov05, sep='\t')
    # df_thousg_svafotate05.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov05']
    # df_thousg_svafotate07 = pd.read_csv(args.svafotate_thousg_ov07, sep='\t')
    # df_thousg_svafotate07.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov07']
    # df_thousg_svafotate09 = pd.read_csv(args.svafotate_thousg_ov09, sep='\t')
    # df_thousg_svafotate09.columns = [COL_NAME_SVID, COL_NAME_SVAFOTATE_AF + '_ov09']
    df_thousg_needlr05 = pd.read_csv(args.needlr_thousg_ov05, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_thousg_needlr05.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov05']
    df_thousg_needlr07 = pd.read_csv(args.needlr_thousg_ov07, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_thousg_needlr07.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov07']
    df_thousg_needlr09 = pd.read_csv(args.needlr_thousg_ov09, sep='\t', usecols=[0, COL_IDX_NEEDLR_AF])
    df_thousg_needlr09.columns = [COL_NAME_SVID, COL_NAME_NEEDLR_AF + '_ov09']
    dfs2merge = [
            df_thousg_stixlrmr1,
            df_thousg_stixlrmr5,
            # df_thousg_svafotate05,
            # df_thousg_svafotate07,
            # df_thousg_svafotate09,
            df_thousg_needlr05,
            df_thousg_needlr07,
            df_thousg_needlr09
    ]
    print("# merging 1000G")
    merged = reduce(
        lambda left, right: left.merge(right, on=COL_NAME_SVID, how="inner"),
        dfs2merge
    )
    merged.to_csv('thousg-merge.tsv', sep='\t')
    ### colo germline
    df_colo_germline_stixlrmr1 = pd.read_csv(args.stixlr_colo_germline_mr1, sep='\t')
    df_colo_germline_stixlrmr1.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr1']
    df_colo_germline_stixlrmr5 = pd.read_csv(args.stixlr_colo_germline_mr5, sep='\t')
    df_colo_germline_stixlrmr5.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr5']
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
    merged = reduce(
        lambda left, right: left.merge(right, on=COL_NAME_SVID, how="inner"),
        dfs2merge
    )
    merged.to_csv('colo_germline-merge.tsv', sep='\t')
    ### colo somatic
    df_colo_somatic_stixlrmr1 = pd.read_csv(args.stixlr_colo_somatic_mr1, sep='\t')
    df_colo_somatic_stixlrmr1.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr1']
    df_colo_somatic_stixlrmr5 = pd.read_csv(args.stixlr_colo_somatic_mr5, sep='\t')
    df_colo_somatic_stixlrmr5.columns = [COL_NAME_SVID, COL_NAME_STIXLR_SAMPLES + '_mr5']
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
    merged = reduce(
        lambda left, right: left.merge(right, on=COL_NAME_SVID, how="inner"),
        dfs2merge
    )
    merged.to_csv('colo_somatic-merge.tsv', sep='\t')





    

if __name__ == "__main__":
    main()
