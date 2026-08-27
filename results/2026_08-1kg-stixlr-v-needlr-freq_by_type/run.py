#!/usr/bin/env python3

import argparse
from cyvcf2 import VCF
import pandas as pd

parser = argparse.ArgumentParser()
# parser.add_argument("--vcf", default='../../data/2026_08-thousg_svs/1KGP_3202.gatksv_svtools_novelins.freeze_V3.wAF.vcf.gz', help="1000 genomes vcf used in stix query")
parser.add_argument("--vcf", default='../../data/2026_08-thousg_svs/1KGP.subset.vcf.gz', help="1000 genomes vcf used in stix query")
parser.add_argument("--popfreqs", default='../2026_08-frequency_benchmark_summary/thousg-merge.tsv')
# parser.add_argument("--output_merge", default='thousg-merge-svtype.tsv', help="output merged frequencies with svtype")
parser.add_argument("--output_merge", default='thousg-merge-svtype.subset.tsv', help="output merged frequencies with svtype")
parser.add_argument("--output", default='stixlr-v-needlr-freq_by_type.subset.tsv')
# parser.add_argument("--output", default='stixlr-v-needlr-freq_by_type.tsv')
parser.add_argument("--cached_merged", help="cached merged frequencies with svtype")
args = parser.parse_args()

COL_STIX_POP_FREQ="stix_samples_mr5"
COL_NEEDLR_AF="needlr_af_ov05"
SVTYPES = ["DEL", "DUP", "INS", "INV"]

def main():
	df = pd.read_csv(args.popfreqs, sep="\t")
	if not args.cached_merged:
		vcf = VCF(args.vcf)
		svid2svtype = []
		print("# mapping svid to svtype")
		for v in vcf:
			svid2svtype.append([v.ID, v.INFO['SVTYPE']])
		df_svid2svtype = pd.DataFrame(svid2svtype, columns=["svid", "svtype"])
		print("# merging type with frequencies")
		merged = pd.merge(df, df_svid2svtype, how='left', on=["svid"])
		merged.to_csv(args.output_merge, sep="\t", index=False)
	else:
		print("# reading cached merged frequencies with svtype")
		merged = pd.read_csv(args.cached_merged, sep="\t")
	merged.drop_duplicates(subset=["svid"], inplace=True)
	merged = merged[merged["svtype"].isin(SVTYPES)]

	with open(args.output, "w") as f:
		f.write("svtype\tsv_count\tstixlr_gt_needlr\tstix_lr_gt_needlr_percent\tneedlr_gt_stixlr\tneedlr_gt_stixlr_percent\n")
		for svtype, df_group in merged.groupby("svtype"):
			n = len(df_group)
			stixlr_gt_needlr = (df_group[COL_STIX_POP_FREQ] > df_group[COL_NEEDLR_AF]).sum()
			needlr_gt_stixlr = (df_group[COL_STIX_POP_FREQ] < df_group[COL_NEEDLR_AF]).sum()
			stixlr_gt_needlr_percent = stixlr_gt_needlr / n * 100
			needlr_gt_stixlr_percent = needlr_gt_stixlr / n * 100
			f.write(
				f"{svtype}\t{n}\t{stixlr_gt_needlr}\t{stixlr_gt_needlr_percent:.5f}\t{needlr_gt_stixlr}\t{needlr_gt_stixlr_percent:.5f}\n"
			)
		total_svs = merged.shape[0]
		total_stixlr_gt_needlr = (merged[COL_STIX_POP_FREQ] > merged[COL_NEEDLR_AF]).sum()
		total_needlr_gt_stixlr = (merged[COL_STIX_POP_FREQ] < merged[COL_NEEDLR_AF]).sum()
		total_stixlr_gt_needlr_percent = total_stixlr_gt_needlr / total_svs * 100
		total_needlr_gt_stixlr_percent = total_needlr_gt_stixlr / total_svs * 100
		f.write(
			"{0}\t{1}\t{2}\t{3:.5f}\t{4}\t{5:.5f}".format(
				"Total", total_svs, total_stixlr_gt_needlr, total_stixlr_gt_needlr_percent,
				total_needlr_gt_stixlr, total_needlr_gt_stixlr_percent
			)
		)


if __name__ == "__main__":
    main()