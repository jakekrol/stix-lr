#!/usr/bin/env python3

import argparse
import os,sys
import pandas as pd
import time

t_0= time.time()
parser = argparse.ArgumentParser(description="make VCF from stix lr cosmic data")
parser.add_argument("--input", required=True, help="Input tsv file with cosmic SVs")
parser.add_argument("--output", required=True, help="Output VCF file")

HEADER="""
##fileformat=VCFv4.2
##contig=<ID=1,length=248956422>
##contig=<ID=2,length=242193529>
##contig=<ID=3,length=198295559>
##contig=<ID=4,length=190214555>
##contig=<ID=5,length=181538259>
##contig=<ID=6,length=170805979>
##contig=<ID=7,length=159345973>
##contig=<ID=8,length=145138636>
##contig=<ID=9,length=138394717>
##contig=<ID=10,length=133797422>
##contig=<ID=11,length=135086622>
##contig=<ID=12,length=133275309>
##contig=<ID=13,length=114364328>
##contig=<ID=14,length=107043718>
##contig=<ID=15,length=101991189>
##contig=<ID=16,length=90338345>
##contig=<ID=17,length=83257441>
##contig=<ID=18,length=80373285>
##contig=<ID=19,length=58617616>
##contig=<ID=20,length=64444167>
##contig=<ID=21,length=46709983>
##contig=<ID=22,length=50818468>
##contig=<ID=23,length=156040895>
##contig=<ID=24,length=57227415>
##contig=<ID=X,length=156040895>
##contig=<ID=Y,length=57227415>
##ALT=<ID=DEL,Description="Deletion">
##ALT=<ID=INS,Description="Insertion">
##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variation">
##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Length of structural variation">
##INFO=<ID=END,Number=1,Type=Integer,Description="End position of structural variation">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO
"""

def validate(args):
    assert os.path.exists(args.input), f"Input file does not exist: {args.input}"

def sex_chr_map(chrom):
    if chrom == '23':
        return 'X'
    elif chrom == '24':
        return 'Y'
    else:
        return chrom

def bedrow2vcfline(row):
    chrom = row['chrom']
    chrom = sex_chr_map(chrom)
    pos = row['start']
    end = row['end']
    if end > pos:
        sv_type = "DEL"
    else:
        sv_type = "INS"
    # negative for DEL and positive for INS
    sv_len = -(end - pos)
    vcf_line = f"{chrom}\t{pos}\t.\tN\t<{sv_type}>" \
        f"\t.\t.\tSVTYPE={sv_type};SVLEN={sv_len};END={end}"
    return vcf_line

def main():
    # args
    args = parser.parse_args()
    validate(args)
    # input
    print(f"# reading input file: {args.input}")
    df = pd.read_csv(args.input, sep="\t")
    df.columns = ['chrom', 'start', 'end', 'sv_type', 'sample_count']

    # output
    print(f"# writing output vcf: {args.output}")
    with open(args.output, 'w') as out_f:
        out_f.write(HEADER.strip() + "\n")
        for _, row in df.iterrows():
            vcf_line = bedrow2vcfline(row)
            out_f.write(vcf_line + "\n")
    print(f"# vcf saved to {args.output}")
    print(f"# elapsed time: {time.time()-t_0:.3f} seconds")

if __name__ == "__main__":
    main()  
