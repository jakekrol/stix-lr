#!/usr/bin/env bash

data_dir="../../data/2026_04-mosaic_ryan"
script="../../src/build_null.py"

# ref
python "$script" \
    -i "$data_dir/sr_lr_agg.allele_ballance.refs.tsv" \
    -o null_ref.npy
# het alt
python "$script" \
    -i "$data_dir/sr_lr_agg.allele_ballance.hets.tsv" \
    -o null_het.npy