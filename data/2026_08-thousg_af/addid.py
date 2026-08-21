#!/usr/bin/env python3

import argparse
from cyvcf2 import VCF
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--vcf", default='../2026_08-thousg_svs/1KGP_3202.gatksv_svtools_novelins.freeze_V3.wAF.vcf.gz')
parser.add_argument('--bed', default='./1kg_pop_freq.lr_samples.bed')
parser.add_argument("--output", default='thousg-sample_counts-addID.tsv')
args = parser.parse_args()

def main():
	vcf = VCF(args.vcf)
	df = pd.read_csv(args.bed, sep="\t")
	df.columns = ["chrom", "start", "end", "svtype", "thousg_samples"]
	vcf_data=[]
	print("# mapping svid to svtype")
	for v in vcf:
			chrom = v.CHROM
			start = v.POS
			svtype = v.INFO['SVTYPE']
			svid = v.ID
			end = v.INFO['END']
			vcf_data.append([chrom, start, end, svtype, svid])
	df_vcf = pd.DataFrame(vcf_data, columns=["chrom", "start", "end", "svtype", "svid"])
	print("# merging type with sample counts")
	merged = pd.merge(df, df_vcf, how='outer', on=["chrom", "start", "end", "svtype"])
	merged.dropna(subset=["thousg_samples"], inplace=True)
	merged['thousg_samples'] = merged['thousg_samples'].astype(int)
	merged.to_csv(args.output, sep="\t", index=False)

if __name__ == "__main__":
    main()