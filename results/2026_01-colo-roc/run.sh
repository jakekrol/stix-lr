#!/usr/bin/env bash

# plot script
script=/data/jake/rl-tools/plot/roc.py

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

overlaps=(05 06 07 08 09)
for x in "${overlaps[@]}"; do
    germline_var="svafotate_ov${x}_germline"
    somatic_var="svafotate_ov${x}_somatic"
    comb_var="svafotate_ov${x}_comb"
    # ${!x} syntax means we treat the value of x as a variable name and get its value
    # here we get the file paths stored in those variable names
    cat <(cut -f1 ${!germline_var} | sed 's|$|\t0|') \
        <(cut -f1 ${!somatic_var} | sed 's|$|\t1|') \
        > ${!comb_var}
done

### needlr
dir_needlr=../2026_01-colo-needlr
## germline
needlr_germline="${dir_needlr}/colo_needlr_germline_popfreqs.txt"
## somatic
needlr_somatic="${dir_needlr}/colo_needlr_somatic_popfreqs.txt"
## combined
needlr_comb="needlr-colo-roc.tsv"
cat <(cut -f1 $needlr_germline | sed 's|$|\t0|') \
    <(cut -f1 $needlr_somatic | sed 's|$|\t1|') \
    > $needlr_comb

# plot
$script --scores "${stix_mr1_comb},${stix_mr5_comb},${svafotate_ov05_comb},${svafotate_ov06_comb},${svafotate_ov07_comb},${svafotate_ov08_comb},${svafotate_ov09_comb},${needlr_comb}" \
    --names "STIX-LR;MR=1,STIX-LR;MR=5,SVAFotate;OV=0.5,SVAFotate;OV=0.6,SVAFotate;OV=0.7,SVAFotate;OV=0.8,SVAFotate;OV=0.9,NeedLR" \
    --output stix_lr_vs_svafotate-colo-roc.png \
    --flip \
    --title "COLO829 somatic SV classification"



