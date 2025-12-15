#!/usr/bin/env bash
# svanna db
# wget 'https://zenodo.org/records/17749179/files/2511_hg38.svanna.zip'
# gnomAD
wget 'https://ftp.ncbi.nlm.nih.gov/pub/dbVar/data/Homo_sapiens/by_study/genotype/nstd166/gnomad_v2.1_sv.sites.vcf.gz' \
    -O gnomad_v2.1_sv.sites.vcf.gz

# HGSVC
wget 'http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/HGSVC2/release/v1.0/integrated_callset/freeze3.sv.alt.vcf.gz' \
    -O hgsvc2.freeze3.sv.alt.vcf.gz

# dbSNP
wget 'https://ftp.ncbi.nih.gov/snp/organisms/human_9606_b151_GRCh38p7/VCF/00-common_all.vcf.gz' \
    -O dbSNP.00-common_all.vcf.gz

# DGV
wget 'https://dgv.tcag.ca/dgv/docs/GRCh38_hg38_variants_2020-02-25.txt' \
    -O DGV.GRCh38_hg38_variants_2020-02-25.txt
# supporting
wget 'https://dgv.tcag.ca/dgv/docs/GRCh38_hg38_supportingvariants_2020-02-25.txt' \
    -O DGV.GRCh38_hg38.supportingvariants_2020-02-25.txt
