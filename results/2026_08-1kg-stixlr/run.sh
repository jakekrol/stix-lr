#!/usr/bin/env bash

# conda activate giggle-dev
# ./run.sh 2>&1 | tee run.log
set -euo pipefail

vcf=$(realpath ../../data/2026_08-thousg_svs/1KGP.subset.vcf.gz)
outdir=$(pwd)
timefile=${outdir}/stix_lr-onekg.times
index="/data/jake/stix-lr-grch38"
min_reads=(1 5)

if [ -f "$timefile" ]; then
    echo "# time file $timefile already exists. please remove and rerun."
    exit 1
fi

cd "$index" || { echo "Error: Could not change to directory $index"; exit 1; }

for mr in "${min_reads[@]}"; do
    echo "# running stix lr on $vcf with min reads: $mr"
    outfile="${outdir}/onekg-stix_lr-min_read_${mr}.vcf"
    t_s=$(date +%s)
    stix -B shardfile.txt -s 500 -f "$vcf" -T $mr > "$outfile"
    t_e=$(date +%s)
    t_elapsed=$(( t_e - t_s ))
    echo "# completed in $t_elapsed seconds"
    printf "${outfile}\t${t_elapsed}\n" >> "$timefile"
done

# get pop frequencies for the stix output
for mr in "${min_reads[@]}"; do
    printf "SVID\tSTIX_SAMPLES\n" > "${outdir}/onekg-stix_lr-min_read_${mr}.popfreq.tsv"
    bcftools query -f '%ID\t%INFO/STIX_ONE\n' "${outdir}/onekg-stix_lr-min_read_${mr}.vcf" | sort -k 2,2nr >> "${outdir}/onekg-stix_lr-min_read_${mr}.popfreq.tsv"
done

# compress vcfs
bgzip -c "${outdir}/onekg-stix_lr-min_read_1.vcf" > "${outdir}/onekg-stix_lr-min_read_1.vcf.gz"
bgzip -c "${outdir}/onekg-stix_lr-min_read_5.vcf" > "${outdir}/onekg-stix_lr-min_read_5.vcf.gz"
