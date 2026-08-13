#!/usr/bin/env python3

from cyvcf2 import VCF, Writer
import argparse

parser = argparse.ArgumentParser(description="Add end info to a VCF file")
parser.add_argument("--input_vcf", default='GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.AF.END.gt50bp.vcf')
parser.add_argument("--output_vcf", default='GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.AF.addEND.gt50bp.vcf')
args = parser.parse_args()

def annotate_end(position, length, type):
    if type == "INS":
        return position
    else:
        return position + abs(length)
    
def main():
    vcf = VCF(args.input_vcf)
    w = Writer(args.output_vcf, vcf)
    for i,v in enumerate(vcf):
        if i % 100 == 0:
            print(f"Processed {i} variants")
        end = annotate_end(v.POS, v.INFO.get("SVLEN", 0), v.INFO.get("SVTYPE", ""))
        v.INFO["END"] = end
        w.write_record(v)
    w.close()

if __name__ == "__main__":
    main()