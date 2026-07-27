#!/usr/bin/env bash

url_1000g_vcf='https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/integrated_sv_map/ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz'
url_1000g_vcf_tbi='https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/integrated_sv_map/ALL.wgs.mergedSV.v8.20130502.svs.genotypes.vcf.gz.tbi'

wget "$url_1000g_vcf"
wget "$url_1000g_vcf_tbi"

