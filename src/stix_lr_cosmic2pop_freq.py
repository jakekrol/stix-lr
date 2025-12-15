#!/usr/bin/env python3

import argparse
import os,sys
import pandas as pd
import time

t_0=time.time()
parser = argparse.ArgumentParser(description="Get pop freq for cosmic SVs in stix lr data")
parser.add_argument("--input", required=True, help="Input tsv file with cosmic SVs")
parser.add_argument("--output", required=True, help="Output file with pop frequencies")
parser.add_argument("--pop_size", type=int, default=1104, help="Population size for frequency calculation")

def validation(args):
    assert os.path.exists(args.input), f"Input file does not exist: {args.input}"
    assert args.pop_size > 0, "Population size must be greater than 0"

def main():
    # args
    args = parser.parse_args()
    validation(args)
    # input
    df = pd.read_csv(args.input, sep="\t")
    df.columns = ['chrom', 'start', 'end', 'sv_type', 'sample_count']

    # pop freq
    df['pop_freq'] = df['sample_count'] / args.pop_size

    df.to_csv(args.output, sep="\t", index=False)
    print(f"# pop frequencies saved to {args.output}")
    print(f"# elapsed time: {time.time()-t_0:.3f} seconds")

if __name__ == "__main__":
    main()