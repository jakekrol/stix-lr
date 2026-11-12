#!/usr/bin/env python3

import argparse
from cyvcf2 import VCF
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--vcf", default='../../data/2026_08-thousg_svs/1KGP.subset.vcf.gz',help='subset VCF')
parser.add_argument("--popfreqs", default='../2026_08-frequency_benchmark_summary/thousg-merge.tsv',help='has column for stix-lr 1kg sv pop. freq.s')
parser.add_argument("--output_merge", default='thousg-merge-svtype.tsv', help="frequencies merged with svtype, svlen, etc.")
parser.add_argument("--output_stix_thousg", default='stixlr-v-thousg-freq_by_type.tsv')
parser.add_argument("--output_stix_needlr", default='stixlr-v-needlr-freq_by_type.tsv')
parser.add_argument("--stix_samples",default=1108,help="num. samples in stix lr index")
# parser.add_argument("--cached_merge", help="optional; path to existing output_merge to speed up")
args = parser.parse_args()
args.stix_samples = int(args.stix_samples)

COL_STIX_SAMPLES="stix_samples_mr5" 
COL_THOUSG_SAMPLES="thousg_samples"
COL_NEEDLR_AF='needlr_af_ov05'
SVTYPES = ["DEL", "DUP", "INS", "INV"]

def vcf2tbl(path: str):
	vcf=VCF(path)
	sv_data=[]
	for v in vcf:
		sv_data.append([v.ID, v.INFO['SVTYPE'], v.INFO['SVLEN']])
	df_sv = pd.DataFrame(sv_data,columns=['svid','svtype','svlen'])
	return df_sv

def write_freq_comparison(merged: pd.DataFrame, other: str, out: str):
	if other == 'thousg':
		name_other='thousg'
		col_other=COL_THOUSG_SAMPLES
		# undo normalizatin for sample comparison
		merged[COL_STIX_SAMPLES] = merged[COL_STIX_SAMPLES] * args.stix_samples
	elif other == 'needlr':
		name_other='needlr'
		col_other=COL_NEEDLR_AF
	else:
		raise ValueError
	with open(out, 'w') as f:
		f.write(f"svtype\tsv_count\tstixlr_gt_{name_other}\tstixlr_gt_{name_other}_percent\t{name_other}_gt_stixlr\t{name_other}_gt_stixlr_percent\n")
		for svtype, df_group in merged.groupby("svtype"):
			n = len(df_group)
			stixlr_gt_other = (df_group[COL_STIX_SAMPLES] > df_group[col_other]).sum()
			other_gt_stixlr = (df_group[COL_STIX_SAMPLES] < df_group[col_other]).sum()
			stixlr_gt_other_percent = round(stixlr_gt_other / n * 100, 3)
			other_gt_stixlr_percent = round(other_gt_stixlr / n * 100, 3)
			f.write(
				f"{svtype}\t{n}\t{stixlr_gt_other}\t{stixlr_gt_other_percent:.3f}\t{other_gt_stixlr}\t{other_gt_stixlr_percent:.3f}\n"
			)
		### for type agnostic comparison
		total_svs = merged.shape[0]
		total_stixlr_gt_other = (merged[COL_STIX_SAMPLES] > merged[col_other]).sum()
		total_other_gt_stixlr = (merged[COL_STIX_SAMPLES] < merged[col_other]).sum()
		total_stixlr_gt_other_percent = round(total_stixlr_gt_other / total_svs * 100, 3)
		total_other_gt_stixlr_percent = round(total_other_gt_stixlr / total_svs * 100, 3)
		
		f.write(
			"{0}\t{1}\t{2}\t{3:.3f}\t{4}\t{5:.3f}".format(
				"Total", total_svs, total_stixlr_gt_other, total_stixlr_gt_other_percent,
				total_other_gt_stixlr, total_other_gt_stixlr_percent
				)
			)

def main():
	vcf = VCF(args.vcf)
	df_freq = pd.read_csv(args.popfreqs, sep="\t")
	df_freq[COL_STIX_SAMPLES] = df_freq[COL_STIX_SAMPLES] / args.stix_samples

	print("# getting info from vcf")
	df_sv = vcf2tbl(args.vcf)
	print("# merging vcf data with frequencies")
	merged = pd.merge(df_freq, df_sv, how='left', on="svid")
	merged.to_csv(args.output_merge, sep="\t", index=False)
	merged.drop_duplicates(subset=["svid"], inplace=True)
	merged = merged[merged["svtype"].isin(SVTYPES)]

	write_freq_comparison(merged, 'thousg', args.output_stix_thousg)
	write_freq_comparison(merged, 'needlr', args.output_stix_needlr)


if __name__ == "__main__":
    main()