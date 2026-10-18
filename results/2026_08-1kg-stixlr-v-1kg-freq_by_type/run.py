#!/usr/bin/env python3

import argparse
from cyvcf2 import VCF
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--vcf", default='../../data/2026_08-thousg_svs/1KGP_3202.gatksv_svtools_novelins.freeze_V3.wAF.vcf.gz',help='full VCF')
parser.add_argument("--vcf_sub", default='../../data/2026_08-thousg_svs/1KGP.subset.vcf.gz',help='subset VCF')
parser.add_argument("--stix_prior", default="../2026_08-1kg-stixlr-reuse-add_id/onekg-stix_lr-min_read_5.popfreq.tsv",help="prior stix results from GitHub")
parser.add_argument("--stix_prior_sub", default="../2026_08-1kg-stixlr-reuse-add_id/onekg-stix_lr-min_read_5.popfreq.tsv",help="prior stix results from GitHub (subset vcf)")
parser.add_argument("--popfreqs", default='../2026_08-frequency_benchmark_summary/thousg-merge.tsv',help='has column for stix-lr 1kg sv pop. freq.s')
parser.add_argument("--output_merge", default='thousg-merge-svtype.tsv', help="frequencies merged with svtype, svlen, etc.")
parser.add_argument("--output_merge_sub", default='thousg-merge-svtype.subset.tsv', help="frequencies merged with svtype, svlen, etc. (subset result)")
parser.add_argument("--output", default='stixlr-v-thousg-freq_by_type.tsv',help="table comparing freq.s stix-lr v 1kg")
parser.add_argument("--output_sub", default='stixlr-v-thousg-freq_by_type.subset.tsv', help="table comparing freq.s stix-lr v 1kg (subset result)")
parser.add_argument("--output_prior", default='stixlr-v-thousg-freq_by_type.prior.tsv',help="table comparing freq.s stix-lr v 1kg (use stix results from GitHub)")
parser.add_argument("--output_prior_sub", default='stixlr-v-thousg-freq_by_type.prior.subset.tsv',help="table comparing freq.s stix-lr v 1kg (use stix results from GitHub and subset vcf)")
parser.add_argument("--stix_samples",default=1108,help="num. samples in stix lr index")
# parser.add_argument("--cached_merge", help="optional; path to existing output_merge to speed up")
# parser.add_argument("--cached_merge_sub", help="optional; path to existing output_merge to speed up (subset result)")
args = parser.parse_args()
args.stix_samples = int(args.stix_samples)

COL_STIX_SAMPLES="stix_samples_mr5" # already transformed into freq by div num_samples=1108
COL_THOUSG_AF="thousg_af"
SVTYPES = ["DEL", "DUP", "INS", "INV"]

def vcf2tbl(path: str):
	vcf=VCF(path)
	sv_data=[]
	for v in vcf:
		sv_data.append([v.ID, v.INFO['SVTYPE'], v.INFO['AF'], v.INFO['SVLEN']])
	df_sv = pd.DataFrame(sv_data,columns=['svid','svtype',COL_THOUSG_AF,'svlen'])
	return df_sv

def write_freq_comparison(merged: pd.DataFrame, out: str):
	with open(out, 'w') as f:
		f.write("svtype\tsv_count\tstixlr_gt_thousg\tstixlr_gt_thousg_percent\tthousg_gt_stixlr\tthousg_gt_stixlr_percent\n")
		for svtype, df_group in merged.groupby("svtype"):
			n = len(df_group)
			stixlr_gt_thousg = (df_group[COL_STIX_SAMPLES] > df_group[COL_THOUSG_AF]).sum()
			thousg_gt_stixlr = (df_group[COL_STIX_SAMPLES] < df_group[COL_THOUSG_AF]).sum()
			stixlr_gt_thousg_percent = stixlr_gt_thousg / n * 100
			thousg_gt_stixlr_percent = thousg_gt_stixlr / n * 100
			f.write(
				f"{svtype}\t{n}\t{stixlr_gt_thousg}\t{stixlr_gt_thousg_percent:.5f}\t{thousg_gt_stixlr}\t{thousg_gt_stixlr_percent:.5f}\n"
			)
		### for type agnostic comparison
		# total_svs = merged.shape[0]
		# total_stixlr_gt_thousg = (merged[COL_STIX_SAMPLES] > merged[COL_THOUSG_AF]).sum()
		# total_thousg_gt_stixlr = (merged[COL_STIX_SAMPLES] < merged[COL_THOUSG_AF]).sum()
		# total_stixlr_gt_thousg_percent = total_stixlr_gt_thousg / total_svs * 100
		# total_thousg_gt_stixlr_percent = total_thousg_gt_stixlr / total_svs * 100
		
		# f.write(
		# 	"{0}\t{1}\t{2}\t{3:.5f}\t{4}\t{5:.5f}".format(
		# 		"Total", total_svs, total_stixlr_gt_thousg, total_stixlr_gt_thousg_percent,
		# 		total_thousg_gt_stixlr, total_thousg_gt_stixlr_percent
		# 		)
		# 	)

def main():
	vcf = VCF(args.vcf)
	df_freq = pd.read_csv(args.popfreqs, sep="\t")
	df_stix = pd.read_csv(args.stix_prior,sep="\t")
	df_stix.columns = ['svid', COL_STIX_SAMPLES]
	df_stix[COL_STIX_SAMPLES] = df_stix[COL_STIX_SAMPLES] / args.stix_samples # compute pop. freq
	df_stix_sub = pd.read_csv(args.stix_prior_sub,sep="\t")
	df_stix_sub.columns = ['svid', COL_STIX_SAMPLES]
	df_stix_sub[COL_STIX_SAMPLES] = df_stix_sub[COL_STIX_SAMPLES] / args.stix_samples # compute pop. freq

	### full vcf
	print("# full vcf")
	print("# getting info from vcf")
	df_sv = vcf2tbl(args.vcf)
	print("# merging vcf data with frequencies")
	merged = pd.merge(df_freq, df_sv, how='left', on="svid")
	merged.to_csv(args.output_merge, sep="\t", index=False)
	merged.drop_duplicates(subset=["svid"], inplace=True)
	merged = merged[merged["svtype"].isin(SVTYPES)]
	write_freq_comparison(merged, args.output)
	# repeat for prior stix results
	merged = pd.merge(df_stix, df_sv, how='left', on='svid')
	merged.drop_duplicates(subset=["svid"], inplace=True)
	merged = merged[merged["svtype"].isin(SVTYPES)]
	write_freq_comparison(merged, args.output_prior)

	### subset vcf
	print("# subset vcf")
	print("# getting info from vcf")
	df_sv = vcf2tbl(args.vcf_sub)
	print("# merging vcf data with frequencies")
	merged = pd.merge(df_freq, df_sv, how='left', on="svid")
	merged.to_csv(args.output_merge_sub, sep="\t", index=False)
	merged.drop_duplicates(subset=["svid"], inplace=True)
	merged= merged[merged["svtype"].isin(SVTYPES)]
	write_freq_comparison(merged, args.output_sub)
	# repeat for prior stix results
	merged = pd.merge(df_stix_sub, df_sv, how='left', on='svid')
	merged.drop_duplicates(subset=["svid"], inplace=True)
	merged = merged[merged["svtype"].isin(SVTYPES)]
	write_freq_comparison(merged, args.output_prior_sub)


if __name__ == "__main__":
    main()