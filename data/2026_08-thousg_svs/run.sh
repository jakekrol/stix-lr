#!/usr/bin/env bash

vcf='1KGP_3202.gatksv_svtools_novelins.freeze_V3.wAF.vcf.gz'
vcf_subset="1KGP.subset.vcf.gz"
url='https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000G_2504_high_coverage/working/20210124.SV_Illumina_Integration/1KGP_3202.gatksv_svtools_novelins.freeze_V3.wAF.vcf.gz'

wget "$url"

# keep only sample columns from stix index
# keep only variants with alternate allele count > 0 among the subset samples
bcftools view -S sample_id.unique.txt --force-samples $vcf | \
    bcftools view -i  'AC>0' -O z -o $vcf_subset
     
