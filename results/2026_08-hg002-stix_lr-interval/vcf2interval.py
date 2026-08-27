#!/usr/bin/env python3

import argparse
from jkbiolib.variant.convert import vcf2stix_queries

parser = argparse.ArgumentParser()
parser.add_argument("--input", default="../../data/2026_07-hg002-svs/GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.AF.addEND.gt50bp.vcf.gz", help="vcf")
parser.add_argument("--output", default="hg002-stix_queries.tsv", help="stix queries")
args = parser.parse_args()

def main():
	vcf2stix_queries(args.input, args.output)

if __name__ == "__main__":
    main()