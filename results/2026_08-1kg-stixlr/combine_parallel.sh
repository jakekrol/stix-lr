#!/usr/bin/env bash

set -e

files=(
    $(for i in {1..22}; do echo "parallel_out/1KGP.subset.chr${i}.mr5.vcf"; done)
    parallel_out/1KGP.subset.chrX.mr5.vcf
    parallel_out/1KGP.subset.chrY.mr5.vcf
)
for f in "${files[@]}"; do
    sorted="${f%.vcf}.sort.vcf"
    bcftools sort -Ov -o "$sorted" "$f"
done

files=(
    $(for i in {1..22}; do echo "parallel_out/1KGP.subset.chr${i}.mr5.sort.vcf"; done)
    parallel_out/1KGP.subset.chrX.mr5.sort.vcf
    parallel_out/1KGP.subset.chrY.mr5.sort.vcf
)

bcftools concat \
    -o 1KGP.subset.merged_stix.mr5.vcf.gz \
    -O z \
    "${files[@]}"