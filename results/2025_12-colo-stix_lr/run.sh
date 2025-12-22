#!/usr/bin/env bash
t_0=$(date +%s)

min_reads=(1 5)
for mr in "${min_reads[@]}"; do
  echo "# getting list of min read ${mr} VCF files"

  mapfile -t mr1 < <(ls colo_germline.*.min_read_${mr}.vcf | grep -v "somatic")
  echo "# concatenating min read ${mr} VCFs"
  bcftools concat $(echo ${mr1[@]}) -O v \
    -o colo_germline.min_read_${mr}.concat.vcf
  echo "# sorting concat VCF"
  bcftools sort -o colo_germline.min_read_${mr}.concat.sort.vcf \
    colo_germline.min_read_${mr}.concat.vcf
done

echo "# done in $(( $(date +%s) - t_0 )) seconds"
