#!/usr/bin/env bash

srcdir=$(pwd)
vcf="${srcdir}/../data/2025_12-hg002-cmrg/HG002_GRCh38_difficult_medical_gene_SV_benchmark_v0.01_trusted_SVTYPE.addID.svafotate.vcf"
outdir="${srcdir}/../results/2025_12-hg002_cmrg-stix_lr"
index="/data/jake/stix-lr-grch38"

cd $index || { echo "Error: Could not change to directory $index"; exit 1; }

t=$(date +%s)
min_reads=5
echo "# running stix lr hg002 cmrg with min reads: $min_reads"
outfile="${outdir}/hg002_cmrg.stix_lr.min_read_5.vcf"
if [ -f "$outfile" ]; then
    echo "# output file $outfile already exists, skipping..."
fi
stix -B shardfile.txt -s 500 -f $vcf -T $min_reads > $outfile
echo "# completed in $(( $(date +%s) - t )) seconds"

min_reads=1
t=$(date +%s)
echo "# running stix lr hg002 cmrg with min reads: $min_reads"
outfile="${outdir}/hg002_cmrg.stix_lr.min_read_1.vcf"
if [ -f "$outfile" ]; then
    echo "# output file $outfile already exists, skipping..."
fi
stix -B shardfile.txt -s 500 -f $vcf -T $min_reads > $outfile
echo "# completed in $(( $(date +%s) - t )) seconds"
