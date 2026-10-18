#!/usr/bin/env python3
import argparse
from cyvcf2 import VCF
import pandas as pd

parser = argparse.ArgumentParser("Use STIX regions to lookup SVID from vcf")
parser.add_argument("--vcf", default='../../data/2026_08-thousg_svs/1KGP_3202.gatksv_svtools_novelins.freeze_V3.wAF.vcf.gz', help="full vcf")
parser.add_argument("--vcf_sub", default='../../data/2026_08-thousg_svs/1KGP.subset.vcf.gz', help="subset vcf")
parser.add_argument("--stix", default='../../data/2026_08-thousg-stix-lr/lr_1kg_pop_freq_t_5.bed', help="STIX samples bed")
parser.add_argument("--output", default='lr_1kg_pop_freq_t_5.addID.bed', help="output full")
parser.add_argument("--output_sub", default='lr_1kg_pop_freq_t_5.addID.subset.bed', help="output subset")
args = parser.parse_args()

def vcf2tbl(path: str):
	vcf=VCF(path)
	data_vcf = []
	for v in vcf:
		chrom = v.CHROM
		start = v.POS
		svtype = v.INFO['SVTYPE']
		svid = v.ID
		if svtype == 'INS':
			# stix rule is that END for INS is just +10bp of start POS
			end = start + 10
		else:
			end = v.INFO['END']
		data_vcf.append([chrom, start, end, svtype, svid])
	return pd.DataFrame(data_vcf,columns=['chrom','start','end','svtype','svid'])

def main():
	df = pd.read_csv(args.stix, sep="\t")
	df.columns = ["chrom", "start", "end", "svtype", "stix_samples"]
	### full vcf
	df_vcf=vcf2tbl(args.vcf)
	merged = pd.merge(df, df_vcf, how='left', on=["chrom", "start", "end", "svtype"])
	merged.to_csv(args.output, sep="\t", index=False)
	### subset vcf
	df_vcf=vcf2tbl(args.vcf_sub)
	merged = pd.merge(df, df_vcf, how='left', on=["chrom", "start", "end", "svtype"])
	merged.to_csv(args.output_sub, sep="\t", index=False)


if __name__ == "__main__":
    main()