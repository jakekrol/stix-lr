#!/usr/bin/env python3
import sys
import os
import argparse
import time
from functions import get_conda_exe_path
from functions import extract_maxaf

parser = argparse.ArgumentParser(description="Run svafotate on HG002 CMRG VCF")
parser.add_argument("--input", required=True, help="Input VCF file")
parser.add_argument("--outdir", required=True, help="Output directory")
parser.add_argument("--env_name", default="svafotate-env", help="Conda environment name for SVAFotate")
parser.add_argument("--bed", required=True, help="SVAFotate BED file")
parser.add_argument("--timefile", default=None, help="Optional time log file")
# /data/jake/stix-lr/data/2025_11-svafotate_bed/SVAFotate_core_SV_popAFs.GRCh38.v4.1.bed.gz
args = parser.parse_args()
overlaps = ["0.5", "0.6", "0.7", "0.8", "0.9"]

def validate_args(args):
  assert os.path.exists(args.input), f"Input VCF file {args.input} does not exist"
  assert os.path.exists(args.outdir), f"Output directory {args.outdir} does not exist"
  assert not (args.timefile and os.path.exists(args.timefile)), f"time file already exists at {args.timefile}, please remove or specify a different file"
  assert os.path.exists(args.bed), f"SVAFotate BED file {args.bed} does not exist"

def run_svafotate(cln_vcf, bed_file, outfile, cpus, env_name, overlap, source, timefile=None):
    # Use direct path to svafotate executable instead of conda activate
    svafotate_exe = get_conda_exe_path(env_name, 'svafotate')
    if source != "all":
        cmd = f"{svafotate_exe} annotate -v {cln_vcf} -b {bed_file} " \
            f"-f {overlap} -s {source} -O vcf -o {outfile} --cpu {cpus}"
    else:
        cmd = f"{svafotate_exe} annotate -v {cln_vcf} -b {bed_file} "\
            f"-f {overlap} -O vcf -o {outfile} --cpu {cpus}"
    print("Running cmd:", cmd)
    t_s=time.time()
    result = os.system(cmd)
    t_e=time.time()
    if timefile:
        with open(timefile, 'a') as tf:
            tf.write(f"svafotate_overlap_{overlap}_source_{source}\t{t_e - t_s:.4f}\n")
    if result != 0:
        print(f"Error running svafotate for {cln_vcf}: exit code {result}")
    return outfile

def main():
  t_0 = time.time()
  validate_args(args)
  for overlap in overlaps:
    out_vcf = os.path.join(args.outdir, f"svafotate-hg002-cmrg-overlap_{overlap}.vcf")
    print(f"# running SVAFotate for overlap {overlap}")
    svafotate_vcf = run_svafotate(
        args.input,
        args.bed,
        out_vcf,
        cpus=1,
        env_name=args.env_name,
        overlap=overlap,
        source="all",
        timefile=args.timefile
    )
    print(f"# svafotate output vcf: {svafotate_vcf}")
    # extract Max_AF
    maxaf_out = out_vcf.replace(".vcf", f"_maxpopfreq.txt")
    with open(maxaf_out, 'w') as mf:
      mf.write("svid\tmax_popfreq\n")
    extract_maxaf(svafotate_vcf, maxaf_out, mode='a')
    print(f"# extracted Max_AF to: {maxaf_out}")
  t_end = time.time()
  print("# completed in %.3f seconds" % (t_end - t_0))
  
if __name__ == "__main__":
    main()


  