#!/usr/bin/env bash

# see github.com/jakekrol/rl-tools/plot/density.py
script=/data/jake/rl-tools/plot/density.py
# num samples in stix lr index to normalize counts in to frequencies
POPSIZE=1108

#### inputs

### stix lr
dir_hg002_stix=../2025_12-hg002_cmrg-stix_lr
hg002_stix_min_read1=$dir_hg002_stix/hg002_cmrg.stix_lr.min_read_1.popfreq.tsv
hg002_stix_min_read5=$dir_hg002_stix/hg002_cmrg.stix_lr.min_read_5.popfreq.tsv
### svafotate
dir_hg002_svafotate=../2025_12-hg002_cmrg-svafotate
hg002_svafotate_ov05=$dir_hg002_svafotate/svafotate-hg002-cmrg-overlap_0.5_maxpopfreq.txt
hg002_svafotate_ov06=$dir_hg002_svafotate/svafotate-hg002-cmrg-overlap_0.6_maxpopfreq.txt
hg002_svafotate_ov07=$dir_hg002_svafotate/svafotate-hg002-cmrg-overlap_0.7_maxpopfreq.txt
hg002_svafotate_ov08=$dir_hg002_svafotate/svafotate-hg002-cmrg-overlap_0.8_maxpopfreq.txt
hg002_svafotate_ov09=$dir_hg002_svafotate/svafotate-hg002-cmrg-overlap_0.9_maxpopfreq.txt
### needlr
dir_hg002_needlr=../2026_01-hg002-needlr
hg002_needlr=$dir_hg002_needlr/hg002_needlr_popfreqs.txt

# transform stix sample counts to population frequencies
tail -n +2 $hg002_stix_min_read1 | \
    awk -v ps=$POPSIZE 'BEGIN{OFS="\t"} {print $2/ps}' | \
    sort -nr > hg002-stix_lr-min_read1-popfreqs.txt
tail -n +2 $hg002_stix_min_read5 | \
    awk -v ps=$POPSIZE 'BEGIN{OFS="\t"} {print $2/ps}' | \
    sort -nr > hg002-stix_lr-min_read5-popfreqs.txt

# extract popfreq column for svafotate files
for x in 05 06 07 08 09; do
    infile="hg002_svafotate_ov${x}"
    outfile="hg002-svafotate-ov${x}-popfreqs.txt"
    tail -n +2 ${!infile} | cut -f2 | sort -gr > $outfile
done

# plot density distributions
python $script \
    --figsize 10 5 \
    --inputs "hg002-stix_lr-min_read1-popfreqs.txt,hg002-stix_lr-min_read5-popfreqs.txt,hg002-svafotate-ov05-popfreqs.txt,hg002-svafotate-ov06-popfreqs.txt,hg002-svafotate-ov07-popfreqs.txt,hg002-svafotate-ov08-popfreqs.txt,hg002-svafotate-ov09-popfreqs.txt,$hg002_needlr" \
    --names "STIX-LR;MR=1,STIX-LR;MR=5,SVAFotate;OV=0.5,SVAFotate;OV=0.6,SVAFotate;OV=0.7,SVAFotate;OV=0.8,SVAFotate;OV=0.9,NeedLR" \
    --title "HG002 CMRG SV Population Frequency Distributions" \
    --xlabel "" \
    --ylabel "Population frequency" \
    --show_median \
    --output "hg002-cmrg-popfreq-density.png"






