#!/usr/bin/env python3

import argparse
import cyvcf2
from cyvcf2 import VCF, Writer
import multiprocessing
from multiprocessing import Pool
import os
import sys
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("--vcf", default="../../data/2026_08-thousg_svs/1KGP.subset.vcf.gz")
parser.add_argument("--dir_index",default="/data/jake/stix-lr-grch38")
parser.add_argument("--dir_out", default="parallel_out")
parser.add_argument("--conda_stix", default="polymerization", help="conda environment to init before running stix")
parser.add_argument("--max_cpus", default=30)
parser.add_argument("--slop", default=500)
parser.add_argument("--log", default="run_parallel.log")
args = parser.parse_args()

MIN_READS=[5,1]
SHARDFILE="shardfile.txt"
SPLIT_NAME_PREFIX="1KGP.subset."

def validate_args() -> None:
    os.makedirs(args.dir_out,exist_ok=True)
    assert os.path.exists(args.dir_index)
    assert os.path.exists(args.vcf)
    args.max_cpus = int(args.max_cpus)
    args.slop = int(args.slop)

def split_by_chrom(
    vcf: cyvcf2.VCF,
    dir_out: str,
    name_prefix: str,
    name_suffix: str = ".vcf.gz"
) -> list [str]:
    writers={}
    split_vcfs=[]
    for variant in vcf:
        chrom=variant.CHROM
        if chrom not in writers:
            outfile=f"{name_prefix}{chrom}{name_suffix}"
            writers[chrom]=Writer(
                fname=outfile, tmpl=vcf, mode="wz"
            )
            split_vcfs.append(outfile)
        writers[chrom].write_record(variant)
    for writer in writers.values():
        writer.close()
    return split_vcfs

def run_stix(
    path_vcf: str,
    dir_index: str,
    slop: int,
    min_reads: int,
    path_shardfile: str,
    path_out: str,
    conda_env: str
) -> tuple[int, float, str]:
    cmd = f"cd {dir_index} && stix -f {path_vcf} -s {slop} -T {min_reads} -B {path_shardfile} > {path_out}"
    if conda_env:
        # init conda by sourcing bashrc
        leading = f"source ~/.bashrc; conda activate {conda_env}; "
        cmd = leading + cmd
    print(f"# running cmd: {cmd}")
    t_0=time.time()
    result=subprocess.run(
        cmd, shell=True, check=True, text=True
    )
    t_elapsed=time.time()-t_0
    print(f"# cmd {cmd}; result {result.returncode}")
    return result.returncode, t_elapsed, cmd

def main():
    validate_args()
    vcf=VCF(args.vcf)
    print("# splitting input vcf by chromosome")
    split_vcfs = split_by_chrom(
        vcf=vcf, dir_out=".", name_prefix=SPLIT_NAME_PREFIX, 
    )
    for min_read in MIN_READS:
        queries = []
        for split_vcf in split_vcfs:
            outfile=os.path.basename(split_vcf).replace('.vcf.gz', f".mr{min_read}.vcf")
            outfile=os.path.join(
                args.dir_out,
                outfile
            )
            outfile=os.path.realpath(outfile)
            split_vcf=os.path.realpath(split_vcf)
            queries.append(
                (
                    split_vcf,
                    args.dir_index,
                    args.slop,
                    min_read,
                    SHARDFILE,
                    outfile,
                    args.conda_stix
                )
            )
                
        processes = min(len(split_vcfs), args.max_cpus)
        with Pool(processes=processes) as pool:
            results=pool.starmap(run_stix,queries)
    print("# final results")
    with open(args.log, "w") as f:
        f.write("return_code\tseconds\tcommand\n")
        for return_code, t_elapsed, cmd in results:
            f.write(f"{return_code}\t{t_elapsed}\t{cmd}\n")

if __name__=="__main__":
    main()
    