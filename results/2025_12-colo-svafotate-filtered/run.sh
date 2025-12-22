#!/usr/bin/env bash
set -euo pipefail
t_0="$(date +%s)"
somatic_gt00_ids='../2025_12-colo-filtered/colo829_somatic_grch38_gt00_ids.txt'
somatic_merge_ids='../2025_12-colo-filtered/somatic_merge_ids.txt'
prefix_germline='../2025_11-colo_svafotate/germline/svafotate-overlap_'
prefix_somatic='../2025_11-colo_svafotate/somatic/svafotate-overlap_'
suffix='-source_all.vcf'
overlaps=(0.5 0.6 0.7 0.8 0.9)
for ov in "${overlaps[@]}"; do
    input_somatic="${prefix_somatic}${ov}${suffix}"
    input_germline="${prefix_germline}${ov}${suffix}"
    echo "# somatic filtering for overlap threshold: $ov"
    bcftools view --exclude 'ID=@'"$somatic_gt00_ids"'' "$input_somatic" -o svafotate.colo_somatic.vcf -O v
    echo "# excluding somatic IDs from germline file for overlap threshold: $ov"
    bcftools view --exclude 'ID=@'"$somatic_merge_ids"'' "$input_germline" -o svafotate.colo_germline.vcf -O v
    echo "# extracting sample counts for overlap threshold: $ov"
    ../../src/svafotateout2svid_maxaf.py \
        --input svafotate.colo_somatic.vcf \
        --output svafotate.colo_somatic.svid_popfreq.ov${ov}.txt \
        --add_header
    ../../src/svafotateout2svid_maxaf.py \
        --input svafotate.colo_germline.vcf \
        --output svafotate.colo_germline.svid_popfreq.ov${ov}.txt \
        --add_header
done
echo "# done. elapsed time: $(( $(date +%s) - t_0 )) seconds"
