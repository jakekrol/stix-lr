#!/usr/bin/env bash

input_somatic=../../data/2025_11-colo_sv_calls/colo829_benchmark_grch38.vcf
input_merge=../../data/2025_11-colo_sv_calls/colo829_merge_grch38.vcf
output_somatic_filt=colo829_somatic_grch38_nogt00.vcf
output_somatic_gt00_ids=colo829_somatic_grch38_gt00_ids.txt
output_somatic_bnd_ids=colo829_somatic_grch38_bnd_ids.txt

echo "# filtering somatic VCF to exclude GT=0/0 calls"
bcftools view --exclude 'GT="0/0"' "$input_somatic" -o "$output_somatic_filt" -O v

echo "# extracting IDs of excluded GT=0/0 calls"
bcftools query -f '%ID\n' --include 'GT="0/0"' "$input_somatic" > "$output_somatic_gt00_ids"

echo "# identifying BND variants for filtering"
bcftools query -f '%ID\n' --include 'INFO/SVTYPE="BND"' "$input_somatic" > "$output_somatic_bnd_ids"

echo "# identifying IDs of somatic SVs in merge file"
# exclude BNDs and get positions
bcftools view --exclude 'ID=@'"$output_somatic_bnd_ids"'' "$input_somatic" | \
  bcftools query -f '%CHROM\t%POS\t%INFO/END\n' > somatic_regions_no_bnd.bed
echo "# compressing and indexing merge file"
bgzip -c "$input_merge" > "$input_merge".gz
tabix -p vcf "$input_merge".gz

echo "# getting somatic merge IDs overlapping somatic regions"
bcftools view -R somatic_regions_no_bnd.bed "$input_merge".gz | \
    bcftools query -f '%ID\n' > somatic_merge_ids.txt

echo "# filtering merge file to exclude somatic SV IDs"
bcftools view --exclude 'ID=@somatic_merge_ids.txt' "$input_merge" -o colo829_germline.vcf -O v


