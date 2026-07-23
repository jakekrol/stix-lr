#!/usr/bin/env python3

import argparse
import pandas as pd


CHROM_COL=1 - 1
START_COL=2 - 1
END_COL=3 - 1
SVTYPE_COL=7 - 1
POP_FREQ_COL=43 - 1

parser = argparse.ArgumentParser(description="Convert a needlr output file to bed format")
parser.add_argument("-i", "--input", help="Input needlr output file")
parser.add_argument("-o", "--output", help="Output bed file")
args = parser.parse_args()

with open(args.input, "r") as f:
    # skip line 1
    next(f)
    with open(args.output, "w") as out:
        for line in f:
            fields = line.strip().split("\t")
            chrom = fields[CHROM_COL]
            if chrom.startswith("chr"):
                chrom = chrom[3:]
            start = fields[START_COL]
            end = fields[END_COL]
            svtype = fields[SVTYPE_COL]
            pop_freq = fields[POP_FREQ_COL]
            out.write(f"{chrom}\t{start}\t{end}\t{svtype}\t{pop_freq}\n")

