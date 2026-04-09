#!/usr/bin/env python3

import argparse
import os
import pandas as pd

# i noticed stix insertions from vcfs are parsed into queries using this format:
# - POS = left.start = left.end = right.start
# - right.end = POS+SVLEN

parser=argparse.ArgumentParser(description="Format vcf insertion data for stix lr querying")
parser.add_argument("--input", help="input tsv file")
parser.add_argument("--output", help="output tsv file")
args=parser.parse_args()

df = pd.read_csv(args.input, sep="\t")
df_out = df.copy()

df_out['chrom'] = df_out['CHROM'].str.replace("chr", "")
df_out['left_start'] = df_out['POS']
df_out['left_end'] = df_out['POS']
df_out['right_start'] = df_out['POS']
df_out['right_end'] = df_out['POS'] + df_out['SVLEN']
df_out['svtype'] = 'INS'
df_out['outfile'] = df['ID'] + '.stix.depths'
df_out = df_out[['ID', 'chrom', 'left_start', 'left_end', 'right_start', 'right_end', 'svtype', 'SVLEN', 'outfile']]
df_out.columns = df_out.columns.str.lower()
df_out.to_csv(args.output, sep="\t", index=False)
