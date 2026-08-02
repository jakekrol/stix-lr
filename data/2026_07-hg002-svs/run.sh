#!/usr/bin/env bash

gunzip -c GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.vcf.gz \
    > GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.vcf
# add AF INFO field to header
sed '74a\
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">' GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.vcf \
    > GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.AF.vcf
# add END INFO field to header
sed '74a\
##INFO=<ID=END,Number=1,Type=Integer,Description="End position of structural variation">' GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.AF.vcf \
    > GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.AF.END.vcf

# filter for SVLEN >= 50bp
bcftools view -i 'abs(INFO/SVLEN)>=50' -O v -o GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.AF.END.gt50bp.vcf \
    GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.AF.END.vcf

bgzip -c GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.AF.END.gt50bp.vcf \
    > GRCh38_HG002-T2TQ100-V1.0_stvar.addID.svafotate.STIXanno_minreads5.AF.END.gt50bp.vcf.gz