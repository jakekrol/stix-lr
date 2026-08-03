#!/usr/bin/env bash

# ./run.sh 2>&1 | tee run.log
set -euo pipefail

vcf=$(realpath ../../data/2026_07-hg002-svs/GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.AF.END.gt50bp.vcf.gz)
outdir=$(pwd)
timefile=${outdir}/stix_lr-colo.times
index="/data/jake/stix-lr-grch38"
min_reads=(1 5)

if [ -f "$timefile" ]; then
    echo "# time file $timefile already exists. please remove and rerun."
    exit 1
fi

cd "$index" || { echo "Error: Could not change to directory $index"; exit 1; }

for mr in "${min_reads[@]}"; do
    echo "# running stix lr on $vcf with min reads: $mr"
    outfile="${outdir}/hg002-stix_lr-min_read_${mr}.vcf"
    t_s=$(date +%s)
    stix -B shardfile.txt -s 500 -f "$vcf" -T $mr > "$outfile"
    t_e=$(date +%s)
    t_elapsed=$(( t_e - t_s ))
    echo "# completed in $t_elapsed seconds"
    printf "${outfile}\t${t_elapsed}\n" >> "$timefile"
done

