#!/usr/bin/env bash

vcf_hg002='../../data/2026_07-hg002-svs/GRCh38_HG002-T2TQ100-V1.0_stvar.AF.vcf.gz'
vcf_hg002_cmrg='../../data/2025_12-hg002-cmrg/HG002_GRCh38_difficult_medical_gene_SV_benchmark_v0.01_trusted_SVTYPE.addID.svafotate.vcf'
vcf_cosmic='../2026_01-cosmic-tsv-to-vcf/cosmic.v103.grch38.vcf'
vcf_colo_somatic='../2025_12-colo-filtered/colo829_somatic_grch38_nogt00.vcf'
vcf_colo_germline='../2025_12-colo-filtered/colo829_germline.vcf'
for vcf in "$vcf_hg002" "$vcf_hg002_cmrg" "$vcf_cosmic" "$vcf_colo_somatic" "$vcf_colo_germline"; do
    if [ ! -f "$vcf" ]; then
        echo "Error: VCF file $vcf does not exist."
        exit 1
    fi
done
outdir_hg002='./hg002_split'
outdir_hg002_cmrg='./hg002_cmrg_split'
outdir_cosmic='./cosmic_split'
outdir_colo_somatic='./colo_somatic_split'
outdir_colo_germline='./colo_germline_split'
mkdir -p "$outdir_hg002" "$outdir_hg002_cmrg" "$outdir_cosmic" "$outdir_colo_somatic" "$outdir_colo_germline"
echo "# splitting hg002 VCF into separate files"
python3 -c "from jkbiolib.variant.vcf import split_vcf; \
split_vcf('$vcf_hg002', '$outdir_hg002');"
echo "# splitting hg002 cmrg VCF into separate files"
python3 -c "from jkbiolib.variant.vcf import split_vcf; \
split_vcf('$vcf_hg002_cmrg', '$outdir_hg002_cmrg');"
echo "# splitting cosmic VCF into separate files"
python3 -c "from jkbiolib.variant.vcf import split_vcf; \
split_vcf('$vcf_cosmic', '$outdir_cosmic');"
echo "# splitting colo somatic VCF into separate files"
python3 -c "from jkbiolib.variant.vcf import split_vcf; \
split_vcf('$vcf_colo_somatic', '$outdir_colo_somatic');"
echo "# splitting colo germline VCF into separate files"
python3 -c "from jkbiolib.variant.vcf import split_vcf; \
split_vcf('$vcf_colo_germline', '$outdir_colo_germline');"
