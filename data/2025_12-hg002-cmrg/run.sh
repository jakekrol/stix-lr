#!/usr/bin/env bash
vcf='HG002_GRCh38_difficult_medical_gene_SV_benchmark_v0.01_trusted_SVTYPE.addID.svafotate.vcf'
vcf_af="${vcf%.vcf}.AF.vcf"
sed '53a\
##INFO=<ID=AF,Number=1,Type=Float,Description="Allele Frequency">' $vcf > $vcf_af
vcf_af_end="${vcf_af%.vcf}.END.vcf"
sed '54a\
##INFO=<ID=END,Number=1,Type=Integer,Description="End position of structural variation">' $vcf_af > $vcf_af_end
bgzip -c $vcf_af_end > ${vcf_af_end}.gz

