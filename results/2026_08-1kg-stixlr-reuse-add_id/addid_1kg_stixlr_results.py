#!/usr/bin/env python3
import argparse
from cyvcf2 import VCF
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--vcf", default='../../data/2026_08-thousg_svs/1KGP_3202.gatksv_svtools_novelins.freeze_V3.wAF.vcf.gz', help="1000 genomes vcf used in stix query")
parser.add_argument("--stix", default='../../data/2026_08-thousg-stix-lr/lr_1kg_pop_freq_t_5.bed', help="STIX results bed")
parser.add_argument("--output", default='lr_1kg_pop_freq_t_5.addID.bed', help="Output bed file")
args = parser.parse_args()

def main():
	vcf = VCF(args.vcf)
	df = pd.read_csv(args.stix, sep="\t")
	df.columns = ["chrom", "start", "end", "svtype", "stix_samples"]
	vcf_data=[]
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
		vcf_data.append([chrom, start, end, svtype, svid])
	df_vcf = pd.DataFrame(vcf_data, columns=["chrom", "start", "end", "svtype", "svid"])
	merged = pd.merge(df, df_vcf, how='outer', on=["chrom", "start", "end", "svtype"])
	merged.dropna(subset=["stix_samples"], inplace=True)
	merged['stix_samples'] = merged['stix_samples'].astype(int)
	merged.to_csv(args.output, sep="\t", index=False)


if __name__ == "__main__":
    main()