#!/usr/bin/env bash
set -euo pipefail
t_0="$(date +%s)"
somatic_gt00_ids='../2025_12-colo-filtered/colo829_somatic_grch38_gt00_ids.txt'
somatic_merge_ids='../2025_12-colo-filtered/somatic_merge_ids.txt'
colo_somatic_stix_min_read_1='../2025_12-colo-stix_lr/colo_somatic.stix_lr.min_read_1.vcf'
colo_somatic_stix_min_read_5='../2025_12-colo-stix_lr/colo_somatic.stix_lr.min_read_5.vcf'
colo_germline_stix_min_read_1='../2025_12-colo-stix_lr/colo_germline.min_read_1.concat.sort.vcf'
colo_germline_stix_min_read_5='../2025_12-colo-stix_lr/colo_germline.min_read_5.concat.sort.vcf'

echo "# somatic filtering"
bcftools view --exclude 'ID=@'"$somatic_gt00_ids"'' "$colo_somatic_stix_min_read_1" -o colo_somatic.min_read_1.vcf -O v
bcftools view --exclude 'ID=@'"$somatic_gt00_ids"'' "$colo_somatic_stix_min_read_5" -o colo_somatic.min_read_5.vcf -O v
echo "# excluding somatic IDs from merge file"
bcftools view --exclude 'ID=@'"$somatic_merge_ids"'' "$colo_germline_stix_min_read_1" -o colo_germline.min_read_1.vcf -O v
bcftools view --exclude 'ID=@'"$somatic_merge_ids"'' "$colo_germline_stix_min_read_5" -o colo_germline.min_read_5.vcf -O v
echo "# extracting sample counts"
../../src/stixlr_vcfout2svid_sample_count.py \
    --input colo_somatic.min_read_1.vcf \
    --output colo_somatic.min_read_1.svid_sample_counts.txt \
    --add_header
../../src/stixlr_vcfout2svid_sample_count.py \
    --input colo_somatic.min_read_5.vcf \
    --output colo_somatic.min_read_5.svid_sample_counts.txt \
    --add_header
../../src/stixlr_vcfout2svid_sample_count.py \
    --input colo_germline.min_read_1.vcf \
    --output colo_germline.min_read_1.svid_sample_counts.txt \
    --add_header
../../src/stixlr_vcfout2svid_sample_count.py \
    --input colo_germline.min_read_5.vcf \
    --output colo_germline.min_read_5.svid_sample_counts.txt \
    --add_header
echo "# done. elapsed time: $(( $(date +%s) - t_0 )) seconds"
