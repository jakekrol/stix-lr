#!/usr/bin/env python3
import argparse
from cyvcf2 import VCF
import pandas as pd

parser = argparse.ArgumentParser(description="SV coord to ID lookup")
parser.add_argument("--vcf", 
                    default="../../data/2026_08-thousg_svs/1KGP.subset.vcf.gz",
                    help="Input VCF file")
parser.add_argument("--bed",
                    default="../../data/2026_08-thousg-stix-lr/lr_1kg_pop_freq_t_5.bed",
                    help="Input BED file")
parser.add_argument("--output", default="onekg-stix_lr-mr5-id.bed", help="Output file")
parser.add_argument("--log", default="run.log", help="Log file")
args = parser.parse_args()

def main():
    vcf_file = args.vcf
    bed_file = args.bed
    output_file = args.output

    # Read VCF file and create a dictionary for SV coordinates to ID mapping
    vcf = VCF(vcf_file)
    df_bed = pd.read_csv(bed_file, sep="\t", header=None, names=["chrom", "start", "end", "svtype", "stix_samples"])
    sv_dict = {}
    for variant in vcf:
        try: 
            chrom = variant.CHROM
            start = variant.POS
            end = variant.INFO.get('END')
            sv_type = variant.INFO.get('SVTYPE')
            # for some reason all of the stix insertion ends are +10bp of start
            if sv_type == 'INS':
                end = start + 10
            sv_id = variant.ID
            sv_key = f"{chrom}-{start}-{end}-{sv_type}"
            sv_dict[sv_key] = sv_id
            # debug code trying to find unmapped variants
            # not found in the vcf, but found in the bed file
            # if (chrom == 'chr11') and (end == 42134928):
            #     breakpoint()
        except Exception as e:
            print(f"Error processing variant {variant.ID}")

            with open(args.log, "a") as f:
                f.write(f"Error processing variant {variant.ID}\n")
                f.flush()

    # Read BED file and map coordinates to SV IDs
    df_bed["coord"] = df_bed.apply(lambda row: f"{row['chrom']}-{row['start']}-{row['end']}-{row['svtype']}", axis=1)
    df_bed["sv_id"] = df_bed["coord"].map(sv_dict).fillna("UnMapped")

    # Write the output to a file
    df_bed.to_csv(output_file, sep="\t", index=False, columns=["chrom", "start", "end", "svtype", "stix_samples", "sv_id"])

if __name__ == "__main__":
    main()
