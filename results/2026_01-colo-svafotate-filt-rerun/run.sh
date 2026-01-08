#!/usr/bin/env bash
# launch from this dir

set -euo pipefail

outdir=$(realpath .)
mkdir -p germline somatic
cd ../../src

# somatic
input=../results/2025_12-colo-filtered/colo829_somatic_grch38_nogt00.vcf
echo "# svafotate somatic, $input"
./exp_svafotate_colo_somatic.py \
  --input $input \
  --bed ../data/2025_11-svafotate_bed/SVAFotate_core_SV_popAFs.GRCh38.v4.1.bed.gz \
  --outdir $outdir/somatic \
  --scriptdir /data/jake/stix-lr/src \
  --cpus 1 \
  --timefile $outdir/svafotate_somatic.time \
  --source_all \
  --env_name svafotate-env 2>&1 | tee $outdir/somatic.log

# germline
input=../results/2025_12-colo-filtered/colo829_germline.vcf
echo "# svafotate germline, $input"
./exp_svafotate_colo_somatic.py \
  --input $input \
  --bed ../data/2025_11-svafotate_bed/SVAFotate_core_SV_popAFs.GRCh38.v4.1.bed.gz \
  --outdir $outdir/germline \
  --scriptdir /data/jake/stix-lr/src \
  --cpus 1 \
  --timefile $outdir/svafotate_germline.time \
  --source_all \
  --env_name svafotate-env 2>&1 | tee $outdir/germline.log 
