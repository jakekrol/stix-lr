#!/usr/bin/env bash

input=$(realpath ../../data/2025_12-hg002-cmrg/HG002_GRCh38_difficult_medical_gene_SV_benchmark_v0.01_trusted_SVTYPE.addID.svafotate.AF.addEND.vcf.gz)
outdir=$(pwd)
timefile=${outdir}/svafotate_hg002_cmrg.times
SVAFOTATE_BED=$(realpath ../../data/2025_11-svafotate_bed/SVAFotate_core_SV_popAFs.GRCh38.v4.1.bed.gz)

cd ../../src && ./svafotate-hg002_cmrg.py \
    --input $input \
    --outdir $outdir \
    --bed $SVAFOTATE_BED \
    --time $timefile \
    --outpattern "svafotate-hg002-cmrg"
