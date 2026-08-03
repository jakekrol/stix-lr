#!/usr/bin/env bash

# see github.com/jakekrol/rl-tools/plot/roc.py
script=/data/jake/rl-tools/plot/roc.py

FILL_MISSING_NEEDLR=0

# combine germline/somatic file pairs

### stix
dir_colo_stix=../2025_12-colo-stix_lr-filtered
## germline
stix_mr1_germline=$dir_colo_stix/stixlr.colo_germline.min_read_1.svid_sample_counts.txt
stix_mr5_germline=$dir_colo_stix/stixlr.colo_germline.min_read_5.svid_sample_counts.txt
## somatic
stix_mr1_somatic=$dir_colo_stix/stixlr.colo_somatic.min_read_1.svid_sample_counts.txt
stix_mr5_somatic=$dir_colo_stix/stixlr.colo_somatic.min_read_5.svid_sample_counts.txt 
## combined files
stix_mr1_comb=stix_lr-colo-roc-min_read_1.tsv
stix_mr5_comb=stix_lr-colo-roc-min_read_5.tsv

cat <(tail -n +2 $stix_mr1_germline | cut -f2  | sed 's|$|\t0|') \
    <(tail -n +2 $stix_mr1_somatic | cut -f2 | sed 's|$|\t1|') \
    > $stix_mr1_comb

cat <(tail -n +2 $stix_mr5_germline | cut -f2  | sed 's|$|\t0|') \
    <(tail -n +2 $stix_mr5_somatic | cut -f2 | sed 's|$|\t1|') \
    > $stix_mr5_comb

### svafotate
dir_colo_svafotate=../2026_01-colo-svafotate-filt-rerun
## germline
svafotate_ov05_germline=$dir_colo_svafotate/germline/svafotate-overlap_0.5-source_all_maxaf.txt
svafotate_ov06_germline=$dir_colo_svafotate/germline/svafotate-overlap_0.6-source_all_maxaf.txt
svafotate_ov07_germline=$dir_colo_svafotate/germline/svafotate-overlap_0.7-source_all_maxaf.txt
svafotate_ov08_germline=$dir_colo_svafotate/germline/svafotate-overlap_0.8-source_all_maxaf.txt
svafotate_ov09_germline=$dir_colo_svafotate/germline/svafotate-overlap_0.9-source_all_maxaf.txt
## somatic
svafotate_ov05_somatic=$dir_colo_svafotate/somatic/svafotate-overlap_0.5-source_all_maxaf.txt
svafotate_ov06_somatic=$dir_colo_svafotate/somatic/svafotate-overlap_0.6-source_all_maxaf.txt
svafotate_ov07_somatic=$dir_colo_svafotate/somatic/svafotate-overlap_0.7-source_all_maxaf.txt
svafotate_ov08_somatic=$dir_colo_svafotate/somatic/svafotate-overlap_0.8-source_all_maxaf.txt
svafotate_ov09_somatic=$dir_colo_svafotate/somatic/svafotate-overlap_0.9-source_all_maxaf.txt
## combined files
svafotate_ov05_comb=svafotate-colo-roc-overlap_0.5.tsv
svafotate_ov06_comb=svafotate-colo-roc-overlap_0.6.tsv
svafotate_ov07_comb=svafotate-colo-roc-overlap_0.7.tsv
svafotate_ov08_comb=svafotate-colo-roc-overlap_0.8.tsv
svafotate_ov09_comb=svafotate-colo-roc-overlap_0.9.tsv

# overlaps=(05 06 07 08 09)
overlaps=(05 07 09)
for x in "${overlaps[@]}"; do
    germline_var="svafotate_ov${x}_germline"
    somatic_var="svafotate_ov${x}_somatic"
    comb_var="svafotate_ov${x}_comb"
    # ${!x} syntax means we treat the value of VAR as a variable name and get its value
    # here we get the file paths stored in those variable names
    cat <(cut -f1 ${!germline_var} | sed 's|$|\t0|') \
        <(cut -f1 ${!somatic_var} | sed 's|$|\t1|') \
        > ${!comb_var}
done

for x in "${overlaps[@]}"; do
    comb_var="svafotate_ov${x}_comb"
    echo "Combined SVAFotate overlap 0.${x} germline/somatic file: ${!comb_var}"
done

### needlr
dir_needlr=../2026_07-colo-needlr
## germline
needlr_germline_05="${dir_needlr}/germline_needLR_ov0.5/needlr_pop_freq.tsv"
needlr_germline_07="${dir_needlr}/germline_needLR_ov0.7/needlr_pop_freq.tsv"
needlr_germline_09="${dir_needlr}/germline_needLR_ov0.9/needlr_pop_freq.tsv"

## somatic
needlr_somatic_05="${dir_needlr}/somatic_needLR_ov0.5/needlr_pop_freq.tsv"
needlr_somatic_07="${dir_needlr}/somatic_needLR_ov0.7/needlr_pop_freq.tsv"
needlr_somatic_09="${dir_needlr}/somatic_needLR_ov0.9/needlr_pop_freq.tsv"
## combined
needlr_comb_05="needlr_ov05_comb.tsv"
needlr_comb_07="needlr_ov07_comb.tsv"
needlr_comb_09="needlr_ov09_comb.tsv"
for x in "${overlaps[@]}"; do
    germline_var="needlr_germline_${x}"
    somatic_var="needlr_somatic_${x}"
    comb_out="needlr_comb_${x}"
    # ${!x} syntax means we treat the value of VAR as a variable name and get its value
    # here we get the file paths stored in those variable names
    cat <(tail -n +2 ${!germline_var} | cut -f2 | sed 's|$|\t0|') \
        <(tail -n +2 ${!somatic_var} | cut -f2 | sed 's|$|\t1|') \
        > ${!comb_out}
    # fill filtered variants (-1) with value
    sed -i "s|-1|${FILL_MISSING_NEEDLR}|g" ${!comb_out}
done


# plot
$script --scores "${stix_mr1_comb},${stix_mr5_comb},${svafotate_ov05_comb},${svafotate_ov07_comb},${svafotate_ov09_comb},${needlr_comb_05},${needlr_comb_07},${needlr_comb_09}" \
    --names "STIX-LR;MR=1,STIX-LR;MR=5,SVAFotate;OV=0.5,SVAFotate;OV=0.7,SVAFotate;OV=0.9,NeedLR;OV=0.5,NeedLR;OV=0.7,NeedLR;OV=0.9" \
    --output colo-stix_lr-svafotate-need_lr-roc.png \
    --flip \
    --title "COLO829 somatic SV classification"

# plot using the new_roc.py formatting
python ./new_roc.py \
    --scores "${stix_mr1_comb},${stix_mr5_comb},${svafotate_ov05_comb},${svafotate_ov07_comb},${svafotate_ov09_comb},${needlr_comb_05},${needlr_comb_07},${needlr_comb_09}" \
    --names "STIX-LR;MR=1,STIX-LR;MR=5,SVAFotate;OV=0.5,SVAFotate;OV=0.7,SVAFotate;OV=0.9,NeedLR;OV=0.5,NeedLR;OV=0.7,NeedLR;OV=0.9" \
    --output colo-stix_lr-svafotate-need_lr-new_roc.png \
    --flip \
    --title "COLO829(BL) SVs"


# count number of zero population frequencies for germline variants for each method
files=("$stix_mr1_comb"
"$stix_mr5_comb"
$svafotate_ov05_comb
$svafotate_ov07_comb 
$svafotate_ov09_comb
$needlr_comb_05
$needlr_comb_07
$needlr_comb_09
)

total_germline_variants=$(awk '$2 == 0' "$stix_mr1_comb" | wc -l)
echo "# total germline variants: $total_germline_variants"
missed_germlines="missed_germlines.tsv"
printf "%s\t%s\n" "file" "num_zero_popfreq_germline" > "$missed_germlines"
for f in "${files[@]}"; do
    echo "Counting number of zero population frequencies for germline variants in $f"
    num_zero=$(awk '$2 == 0' "$f" | awk '$1 <= 0.0' | wc -l)
    frac_zero=$(echo "scale=4; $num_zero / $total_germline_variants" | bc)
    printf "%s\t%s\n" "$f" "$frac_zero" >> "$missed_germlines"
done

