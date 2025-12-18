#!/usr/bin/env python3

import os, sys
from functions import extract_maxaf
import argparse
import time
t_0 = time.time()

parser = argparse.ArgumentParser(description="Extract SVID and Max_AF from svafotate annotated VCF")
parser.add_argument("-i", "--input", required=True, help="Input svafotate annotated VCF file")
parser.add_argument("-o", "--output", required=True, help="Output TSV file for SVID and Max_AF")
parser.add_argument("--add_header", action='store_true', help="Add header line to output file")
args = parser.parse_args() 

def validate(args):
    assert os.path.exists(args.input), f"Input file does not exist: {args.input}"
    outdir = os.path.dirname(args.output)
    assert os.path.exists(outdir), f"Output directory does not exist: {outdir}"
    

def main():
    validate(args)
    if args.add_header:
        with open(args.output, 'w') as outfh:
            outfh.write("svid\tmax_popfreq\n")
    extract_maxaf(
        args.input,
        args.output,
        mode = 'a' if args.add_header else 'w'
    )
    print("# done in %.4f seconds" % (time.time() - t_0))

if __name__ == "__main__":
    main()

