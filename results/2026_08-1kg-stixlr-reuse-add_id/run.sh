#!/usr/bin/env bash

./addid_1kg_stixlr_results.py

awk -v OFS='\t' '{print $6, $5}' lr_1kg_pop_freq_t_5.addID.bed > lr_1kg_pop_freq_t_5.addID.tsv
awk -v OFS='\t' '{print $6, $5}' lr_1kg_pop_freq_t_5.addID.subset.bed > lr_1kg_pop_freq_t_5.addID.subset.tsv