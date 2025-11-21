#!/usr/bin/env bash

# version 2
# somatic SVs
curl 'https://zenodo.org/records/13917379/files/colo829_benchmark_grch38.vcf?download=1' \
    -o 'colo829_benchmark_grch38.vcf'

# germline SVs
curl 'https://zenodo.org/records/10819636/files/colo829_merge_grch38.vcf.gz?download=1' \
    -o 'colo829_merge_grch38.vcf.gz'