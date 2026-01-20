#!/usr/bin/env bash
set -euo pipefail

vcf=$(realpath "../../data/2025_12-hg002-cmrg/HG002_GRCh38_difficult_medical_gene_SV_benchmark_v0.01_trusted_SVTYPE.addID.svafotate.vcf")
if [ ! -f "$vcf" ]; then
    echo "# error: VCF file $vcf not found."
    exit 1
fi
outdir=$(pwd)
index="/data/jake/stix-lr-grch38"
timefile="${outdir}/stix_lr_hg002_cmrg_times.txt"
if [ -f "$timefile" ]; then
    echo "# timefile $timefile already exists, exiting to avoid overwriting."
    exit 0
fi

cd $index || { echo "# error: Could not change to directory $index"; exit 1; }

min_reads=5
echo "# running stix lr hg002 cmrg with min reads: $min_reads"
outfile="${outdir}/hg002_cmrg.stix_lr.min_read_${min_reads}.vcf"
if [ -f "$outfile" ]; then
    echo "# output file $outfile already exists, exiting to avoid overwriting."
    exit 0
fi
t_s=$(date +%s)
stix -B shardfile.txt -s 500 -f $vcf -T $min_reads > $outfile
t_e=$(date +%s)
t_elapsed=$((t_e - t_s))
printf "${outfile}\t${t_elapsed}\n" >> $timefile
echo "# completed in $t_elapsed seconds"

min_reads=1
echo "# running stix lr hg002 cmrg with min reads: $min_reads"
outfile="${outdir}/hg002_cmrg.stix_lr.min_read_${min_reads}.vcf"
if [ -f "$outfile" ]; then
    echo "# output file $outfile already exists, exiting to avoid overwriting."
    exit 0
fi
t_s=$(date +%s)
stix -B shardfile.txt -s 500 -f $vcf -T $min_reads > $outfile
t_e=$(date +%s)
t_elapsed=$((t_e - t_s))
printf "${outfile}\t${t_elapsed}\n" >> $timefile
echo "# completed in $t_elapsed seconds"
