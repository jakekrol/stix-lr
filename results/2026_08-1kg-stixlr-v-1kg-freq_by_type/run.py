#!/usr/bin/env python3

import argparse
from cyvcf2 import VCF
import pandas as pd

parser = argparse.ArgumentParser()
# parser.add_argument("--vcf", default='../../data/2026_08-thousg_svs/1KGP_3202.gatksv_svtools_novelins.freeze_V3.wAF.vcf.gz', help="1000 genomes vcf used in stix query")
parser.add_argument("--vcf", default='../../data/2026_08-thousg_svs/1KGP.subset.vcf.gz', help="1000 genomes vcf used in stix query")
parser.add_argument("--stix", default="../2026_08-1kg-stixlr-reuse-add_id/onekg-stix_lr-min_read_5.popfreq.tsv")
parser.add_argument("--thousg", default="../../data/2026_08-thousg_af/thousg-sample_counts-addID.tsv")
# parser.add_argument("--output_merge", default='thousg-merge-svtype.tsv', help="output merged frequencies with svtype")
parser.add_argument("--output_merge", default='thousg-merge-svtype.subset.tsv', help="output merged frequencies with svtype")
# parser.add_argument("--output", default='stixlr-v-thousg-freq_by_type.tsv')
parser.add_argument("--output", default='stixlr-v-thousg-freq_by_type.subset.tsv')
parser.add_argument("--cached_merge", help="cached merged frequencies with svtype")
args = parser.parse_args()

COL_STIX_SAMPLES="stix_samples"
COL_THOUSG_SAMPLES="thousg_samples"
SVTYPES = ["DEL", "DUP", "INS", "INV"]

def main():
	vcf = VCF(args.vcf)
	df_stix = pd.read_csv(args.stix, sep="\t")
	df_thousg = pd.read_csv(args.thousg, sep="\t")
	df_thousg = df_thousg[["svid", COL_THOUSG_SAMPLES]]
	df = pd.merge(df_stix, df_thousg, how='outer', on='svid')
	df = df.fillna(0)
	if not args.cached_merge:
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
		merged = pd.read_csv(args.cached_merge, sep="\t")
	merged.drop_duplicates(subset=["svid"], inplace=True)
	merged = merged[merged["svtype"].isin(SVTYPES)]

	with open(args.output, "w") as f:
		f.write("svtype\tsv_count\tstixlr_gt_thousg\tstixlr_gt_thousg_percent\tthousg_gt_stixlr\tthousg_gt_stixlr_percent\n")
		for svtype, df_group in merged.groupby("svtype"):
			n = len(df_group)
			stixlr_gt_thousg = (df_group[COL_STIX_SAMPLES] > df_group[COL_THOUSG_SAMPLES]).sum()
			thousg_gt_stixlr = (df_group[COL_STIX_SAMPLES] < df_group[COL_THOUSG_SAMPLES]).sum()
			stixlr_gt_thousg_percent = stixlr_gt_thousg / n * 100
			thousg_gt_stixlr_percent = thousg_gt_stixlr / n * 100
			f.write(
				f"{svtype}\t{n}\t{stixlr_gt_thousg}\t{stixlr_gt_thousg_percent:.5f}\t{thousg_gt_stixlr}\t{thousg_gt_stixlr_percent:.5f}\n"
			)
		total_svs = merged.shape[0]
		total_stixlr_gt_thousg = (merged[COL_STIX_SAMPLES] > merged[COL_THOUSG_SAMPLES]).sum()
		total_thousg_gt_stixlr = (merged[COL_STIX_SAMPLES] < merged[COL_THOUSG_SAMPLES]).sum()
		total_stixlr_gt_thousg_percent = total_stixlr_gt_thousg / total_svs * 100
		total_thousg_gt_stixlr_percent = total_thousg_gt_stixlr / total_svs * 100
		
		f.write(
			"{0}\t{1}\t{2}\t{3:.5f}\t{4}\t{5:.5f}".format(
				"Total", total_svs, total_stixlr_gt_thousg, total_stixlr_gt_thousg_percent,
				total_thousg_gt_stixlr, total_thousg_gt_stixlr_percent
				)
			)


if __name__ == "__main__":
    main()