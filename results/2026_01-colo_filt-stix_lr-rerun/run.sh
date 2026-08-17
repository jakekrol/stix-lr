#!/usr/bin/env bash

# ./run.sh 2>&1 | tee run.log
set -euo pipefail

somatic=$(realpath "../2025_12-colo-filtered/colo829_somatic_grch38_nogt00.vcf")
germline=$(realpath "../2025_12-colo-filtered/colo829_germline.vcf")
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
    for f in "$somatic" "$germline"; do
        if [[ "$f" == *"somatic"* ]]; then
            type="somatic"
        else
            type="germline"
        fi
        echo "# running stix lr on $f with min reads: $mr"
        outfile="${outdir}/colo_${type}-stix_lr-min_read_${mr}.vcf"
        t_s=$(date +%s)
        stix -B shardfile.txt -s 500 -f "$f" -T $mr > "$outfile"
        t_e=$(date +%s)
        t_elapsed=$(( t_e - t_s ))
        echo "# completed in $t_elapsed seconds"
        printf "${outfile}\t${t_elapsed}\n" >> "$timefile"
    done
done

# get pop frequencies for the stix output
X=(germline somatic)
for mr in "${min_reads[@]}"; do
    for x in "${X[@]}"; do
        printf "SVID\tSTIX_SAMPLES\n" > "${outdir}/colo_${x}-stix_lr-min_read_${mr}.popfreq.tsv"
        bcftools query -f '%ID\t%INFO/STIX_ONE\n' "${outdir}/colo_${x}-stix_lr-min_read_${mr}.vcf" | sort -k 2,2nr >> "${outdir}/colo_${x}-stix_lr-min_read_${mr}.popfreq.tsv"
    done
done

bgzip -c colo_germline-stix_lr-min_read_1.vcf > colo_germline-stix_lr-min_read_1.vcf.gz
bgzip -c colo_germline-stix_lr-min_read_5.vcf > colo_germline-stix_lr-min_read_5.vcf.gz
bgzip -c colo_somatic-stix_lr-min_read_1.vcf > colo_somatic-stix_lr-min_read_1.vcf.gz
bgzip -c colo_somatic-stix_lr-min_read_5.vcf > colo_somatic-stix_lr-min_read_5.vcf.gz