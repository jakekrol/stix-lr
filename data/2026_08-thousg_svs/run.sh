#!/usr/bin/env bash

url='https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000G_2504_high_coverage/working/20210124.SV_Illumina_Integration/1KGP_3202.gatksv_svtools_novelins.freeze_V3.wAF.vcf.gz'

wget "$url"

bcftools view -S sample_id.unique.txt --force-samples -o 1KGP.subset.vcf 1KGP_3202.gatksv_svtools_novelins.freeze_V3.wAF.vcf.gz
