#!/usr/bin/env python3

import argparse
from cyvcf2 import VCF
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--vcf", default='../../data/2026_08-thousg_svs/1KGP_3202.gatksv_svtools_novelins.freeze_V3.wAF.vcf.gz', help="1000 genomes vcf used in stix query")
parser.add_argument("--popfreqs", default='../2026_08-frequency_benchmark_summary/thousg-merge.tsv')
parser.add_argument("--output", default='hexbin-stixlr_mr5-thousg_af.png')
parser.add_argument("--cached_merge", help="cached merged frequencies with svtype")
args = parser.parse_args()

COL_STIX_SAMPLES="stix_samples"
COL_THOUSG_AF="thousg_samples"
SVTYPES = ["DEL", "DUP", "INS", "INV"]


def main():
	vcf = VCF(args.vcf)
	df_freq = pd.read_csv(args.popfreqs, sep="\t")
	if not args.cached_merge:
		svid2svtype = []
		print("# mapping svid to svtype")
		for v in vcf:
			svid2svtype.append([v.ID, v.INFO['SVTYPE'], v.INFO['AF'], v.INFO['SVLEN'], v.INFO['SVTYPE']])
		df_svid2svtype = pd.DataFrame(svid2svtype, columns=["svid", "svtype", COL_THOUSG_AF, 'svlen', 'svtype'])
		print("# merging type with frequencies")
		merged = pd.merge(df_freq, df_svid2svtype, how='left', on=["svid"])
		merged.to_csv(args.output_merge, sep="\t", index=False)
	else:
		print("# reading cached merged frequencies with svtype")
		merged = pd.read_csv(args.cached_merge, sep="\t")
	merged.drop_duplicates(subset=["svid"], inplace=True)
	merged = merged[merged["svtype"].isin(SVTYPES)]
	breakpoint()