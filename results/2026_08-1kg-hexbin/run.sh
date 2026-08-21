#!/usr/bin/env bash

### stix-lr v needlr pop. freq.
# stixlr_mr1="../2026_08-1kg-stixlr/onekg-stix_lr-min_read_1.popfreq.tsv"
stixlr_mr5="../2026_08-1kg-stixlr-reuse-add_id/onekg-stix_lr-min_read_5.popfreq.tsv"
needlr_ov05="../2026_08-1kg-needlr/needLR_ov0.5/needlr_pop_freq.tsv"
needlr_ov07="../2026_08-1kg-needlr/needLR_ov0.7/needlr_pop_freq.tsv"
needlr_ov09="../2026_08-1kg-needlr/needLR_ov0.9/needlr_pop_freq.tsv"
cut -f 1,2 $needlr_ov05 > needlr-ov0.5-popfreq.tsv
cut -f 1,2 $needlr_ov07 > needlr-ov0.7-popfreq.tsv
cut -f 1,2 $needlr_ov09 > needlr-ov0.9-popfreq.tsv
cut -f 1,3 $needlr_ov05 > needlr-ov0.5-af.tsv
cut -f 1,3 $needlr_ov07 > needlr-ov0.7-af.tsv
cut -f 1,3 $needlr_ov09 > needlr-ov0.9-af.tsv
needlr_ov05="needlr-ov0.5-popfreq.tsv"
needlr_ov07="needlr-ov0.7-popfreq.tsv"
needlr_ov09="needlr-ov0.9-popfreq.tsv"
# stixlr_files=("$stixlr_mr1" "$stixlr_mr5")
stixlr_files=("$stixlr_mr5")
needlr_files=("$needlr_ov05" "$needlr_ov07" "$needlr_ov09")
for fstix in "${stixlr_files[@]}"; do
    for fneedlr in "${needlr_files[@]}"; do
        mr=$(basename "$fstix" | cut -d '-' -f3 | cut -d '.' -f1 | sed 's|min_read_||')
        ov=$(echo "$fneedlr" | cut -d "/" -f 3 | cut -d '-' -f2 | sed 's|ov||')
        echo "# comparing STIX-LR file $fstix to NEEDLR file $fneedlr"
        echo "# parsed min read: $mr"
        echo "# parsed overlap: $ov"
        ./hex_plot.py \
            --stix $fstix \
            --other $fneedlr \
            --output hexbin-stixlr_mr${mr}-needlr_popfreq_ov${ov}.png \
            --color "Reds" \
            --height 4 \
            --width 5 \
            --xlabel "NeedLR;OV=${ov} population frequency" \
            --ylabel "Num. of samples with STIX long-read depth >= ${mr}" \
            --merged hexbin-stixlr_mr${mr}-needlr_popfreq_ov${ov}.tsv \
            --title "1KG germline SVs"
    done
done


### stix-lr v needlr allele frequency
needlr_ov05="needlr-ov0.5-af.tsv"
needlr_ov07="needlr-ov0.7-af.tsv"
needlr_ov09="needlr-ov0.9-af.tsv"

needlr_files=("$needlr_ov05" "$needlr_ov07" "$needlr_ov09")
for fstix in "${stixlr_files[@]}"; do
    for fneedlr in "${needlr_files[@]}"; do
        mr=$(basename "$fstix" | cut -d '-' -f3 | cut -d '.' -f1 | sed 's|min_read_||')
        ov=$(echo "$fneedlr" | cut -d "/" -f 3 | cut -d '-' -f2 | sed 's|ov||')
        echo "# comparing STIX-LR file $fstix to NEEDLR file $fneedlr"
        echo "# parsed min read: $mr"
        echo "# parsed overlap: $ov"
        ./hex_plot.py \
            --stix $fstix \
            --other $fneedlr \
            --output hexbin-stixlr_mr${mr}-needlr_af_ov${ov}.png \
            --color "Reds" \
            --height 4 \
            --width 5 \
            --xlabel "NeedLR;OV=${ov} AF" \
            --ylabel "Num. of samples with STIX long-read depth >= ${mr}" \
            --merged hexbin-stixlr_mr${mr}-needlr_af_ov${ov}.tsv \
            --title "1KG germline SVs"
    done
done