#!/usr/bin/env bash

wget 'https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/analysis/NIST_HG002_DraftBenchmark_defrabbV0.012-20231107/GRCh38_HG002-T2TQ100-V1.0_stvar.vcf.gz'
gunzip -c GRCh38_HG002-T2TQ100-V1.0_stvar.vcf.gz > GRCh38_HG002-T2TQ100-V1.0_stvar.vcf
# add AF INFO field to header
sed '56a\
##INFO=<ID=AF,Number=1,Type=Float,Description="Allele Frequency">' GRCh38_HG002-T2TQ100-V1.0_stvar.vcf > GRCh38_HG002-T2TQ100-V1.0_stvar.AF.vcf
# add END INFO field to header
# sed -i '56a\
# ##INFO=<ID=END,Number=1,Type=Integer,Description="End position of structural variation">' GRCh38_HG002-T2TQ100-V1.0_stvar.AF.vcf

bgzip -c GRCh38_HG002-T2TQ100-V1.0_stvar.AF.vcf > GRCh38_HG002-T2TQ100-V1.0_stvar.AF.vcf.gz