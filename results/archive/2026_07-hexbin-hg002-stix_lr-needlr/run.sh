#!/usr/bin/env bash


python3.12 ../../src/hex_plot.py \
    --stix ../../data/2026_07-stix_lr-hg002-pop_freqs/lr_1kg_pop_freq_t_5.bed \
    --other ../2026_07-hg002-needlr/hg002_needlr_popfreqs.bed \
    --out stix_lr_mr5-vs-needlr.png \
    --merged stix_lr_mr5-vs-needlr.bed \
    --height 4 \
    --width 5 \
    --color-scale 1,6 \
    --xlabel "SV AF by needLR" \
    --ylabel "Num. of samples with STIX long-read depth => 5" \
    --title "HG002 SVs"