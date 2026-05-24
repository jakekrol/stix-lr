#!/usr/bin/env bash

data_dir="../../data/2026_04-mosaic_ryan"

# annotate
# nboot=1
# script="../../src/mosaic_annotate.py"
# python "$script" \
#     --nulls null_ref.npy null_het.npy \
#     --input ${data_dir}/te_mosiac_agg.allele_ballance.lessmd.rm_missing.tsv \
#     --n-boot 1


# rank
nboot=100
script="./mosaic_rank_parallel.py"
python "$script" \
    --nulls null_ref.npy null_het.npy \
    --input ${data_dir}/te_mosiac_agg.allele_ballance.lessmd.rm_missing.tsv \
    --n-boot 100 \
    --cpus 30 \
    --output mosaic_rank.tsv
