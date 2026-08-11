#!/usr/bin/env bash


stixlr_mr1="../2026_08-hg002-stix_lr/hg002-stix_lr-min_read_1.popfreq.tsv"
stixlr_mr5="../2026_08-hg002-stix_lr/hg002-stix_lr-min_read_5.popfreq.tsv"
needlr_ov05="../2026_07-hg002-needlr/needLR_ov0.5/needlr_pop_freq.tsv"
needlr_ov07="../2026_07-hg002-needlr/needLR_ov0.7/needlr_pop_freq.tsv"
needlr_ov09="../2026_07-hg002-needlr/needLR_ov0.9/needlr_pop_freq.tsv"
cut -f 1,2 $needlr_ov05 > needlr-ov0.5-popfreq.tsv
cut -f 1,2 $needlr_ov07 > needlr-ov0.7-popfreq.tsv
cut -f 1,2 $needlr_ov09 > needlr-ov0.9-popfreq.tsv
cut -f 1,3 $needlr_ov05 > needlr-ov0.5-af.tsv
cut -f 1,3 $needlr_ov07 > needlr-ov0.7-af.tsv
cut -f 1,3 $needlr_ov09 > needlr-ov0.9-af.tsv
needlr_ov05_popfreq="needlr-ov0.5-popfreq.tsv"
needlr_ov07_popfreq="needlr-ov0.7-popfreq.tsv"
needlr_ov09_popfreq="needlr-ov0.9-popfreq.tsv"
needlr_ov05_af="needlr-ov0.5-af.tsv"
needlr_ov07_af="needlr-ov0.7-af.tsv"
needlr_ov09_af="needlr-ov0.9-af.tsv"

### stix-lr v pop. freq needlr
stixlr_files=("$stixlr_mr1" "$stixlr_mr5")
needlr_files=($needlr_ov09_popfreq $needlr_ov07_popfreq $needlr_ov05_popfreq)
for fstix in "${stixlr_files[@]}"; do
    for fneedlr in "${needlr_files[@]}"; do
        mr=$(basename "$fstix" | cut -d '-' -f3 | cut -d '.' -f1 | cut -d '_' -f3)
        ov=$(echo "$fneedlr" | cut -d '-' -f 2 | sed 's|ov||')
        echo "# comparing STIX-LR file $fstix to NEEDLR popfreq file $fneedlr"
        echo "# parsed min read: $mr"
        echo "# parsed overlap: $ov"
        ./hex_plot.py \
            --stix $fstix \
            --other $fneedlr \
            --output hexbin-stixlr_mr${mr}-needlr_popfreq_ov${ov}.png \
            --color Blues \
            --height 4 \
            --width 5 \
            --xlabel "NeedLR;OV=${ov} population frequency" \
            --ylabel "Num. of samples with STIX long-read depth >= ${mr}" \
            --merged hexbin-stixlr_mr${mr}-needlr_popfreq_ov${ov}.tsv \
            --title "HG002 SVs"
    done
done

### stix-lr v af needlr
needlr_files=($needlr_ov09_af $needlr_ov07_af $needlr_ov05_af)
for fstix in "${stixlr_files[@]}"; do
    for fneedlr in "${needlr_files[@]}"; do
        mr=$(basename "$fstix" | cut -d '-' -f3 | cut -d '.' -f1 | cut -d '_' -f3)
        ov=$(echo "$fneedlr" | cut -d '-' -f 2 | sed 's|ov||')
        echo "# comparing STIX-LR file $fstix to NEEDLR af file $fneedlr"
        echo "# parsed min read: $mr"
        echo "# parsed overlap: $ov"
        ./hex_plot.py \
            --stix $fstix \
            --other $fneedlr \
            --output hexbin-stixlr_mr${mr}-needlr_af_ov${ov}.png \
            --color Blues \
            --height 4 \
            --width 5 \
            --xlabel "NeedLR;OV=${ov} AF" \
            --ylabel "Num. of samples with STIX long-read depth >= ${mr}" \
            --merged hexbin-stixlr_mr${mr}-needlr_af_ov${ov}.tsv \
            --title "HG002 SVs"
    done
done


### stix-lr v svafotate
svafotate_ov05='../2026_08-hg002-svafotate/svafotate-hg002_overlap_0.5_maxpopfreq.txt'
svafotate_ov07='../2026_08-hg002-svafotate/svafotate-hg002_overlap_0.7_maxpopfreq.txt'
svafotate_ov09='../2026_08-hg002-svafotate/svafotate-hg002_overlap_0.9_maxpopfreq.txt'
svafotate_files=("$svafotate_ov05" "$svafotate_ov07" "$svafotate_ov09")
for fstix in "${stixlr_files[@]}"; do
    for fsvafotate in "${svafotate_files[@]}"; do
        mr=$(basename "$fstix" | cut -d '-' -f3 | cut -d '.' -f1 | cut -d '_' -f3)
        ov=$(basename "$fsvafotate" | cut -d_ -f3)
        echo "# comparing STIX-LR file $fstix to SVAFotate file $fsvafotate"
        echo "# parsed min read: $mr"
        echo "# parsed overlap: $ov"
        ./hex_plot.py \
            --stix $fstix \
            --other $fsvafotate \
            --output hexbin-stixlr_mr${mr}-svafotate_ov${ov}.png \
            --color Blues \
            --height 4 \
            --width 5 \
            --xlabel "SVAFotate;OV=${ov} population frequency" \
            --ylabel "Num. of samples with STIX long-read depth >= ${mr}" \
            --merged hexbin-stixlr_mr${mr}-svafotate_ov${ov}.tsv \
            --title "HG002 SVs"
    done
done

# ./combine_plots.py