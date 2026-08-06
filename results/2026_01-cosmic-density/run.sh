#!/usr/bin/env bash
set -euo pipefail

# see github.com/jakekrol/rl-tools/plot/density.py
script=./density_and_zero_bar.py
# num samples in stix lr index to normalize counts in to frequencies
POPSIZE=1108
NEEDLR_FILTERED_SV_VALUE=-1

#### inputs

### stix lr
dir_cosmic_stix=../2026_01-cosmic-stix_lr
cosmic_stix_min_read1=$dir_cosmic_stix/cosmic.stix_lr.min_read_1.popfreq.tsv
cosmic_stix_min_read5=$dir_cosmic_stix/cosmic.stix_lr.min_read_5.popfreq.tsv
### svafotate
dir_cosmic_svafotate=../2026_01-cosmic-svafotate
cosmic_svafotate_ov05=$dir_cosmic_svafotate/svafotate-cosmic_overlap_0.5_maxpopfreq.txt
cosmic_svafotate_ov06=$dir_cosmic_svafotate/svafotate-cosmic_overlap_0.6_maxpopfreq.txt
cosmic_svafotate_ov07=$dir_cosmic_svafotate/svafotate-cosmic_overlap_0.7_maxpopfreq.txt
cosmic_svafotate_ov08=$dir_cosmic_svafotate/svafotate-cosmic_overlap_0.8_maxpopfreq.txt
cosmic_svafotate_ov09=$dir_cosmic_svafotate/svafotate-cosmic_overlap_0.9_maxpopfreq.txt
### needlr
cosmic_needlr_ov05=../2026_08-cosmic-needlr/needLR_ov0.5/needlr_pop_freq.tsv
cosmic_needlr_ov07=../2026_08-cosmic-needlr/needLR_ov0.7/needlr_pop_freq.tsv
cosmic_needlr_ov09=../2026_08-cosmic-needlr/needLR_ov0.9/needlr_pop_freq.tsv

# cut the pop freq column from stix files
tail -n +2 $cosmic_stix_min_read1 | cut -f2 | \
    sort -nr > cosmic-stix_lr-min_read1-popfreqs.txt
tail -n +2 $cosmic_stix_min_read5 | cut -f2 | \
   sort -nr > cosmic-stix_lr-min_read5-popfreqs.txt

# extract popfreq column for svafotate files
for x in 05 06 07 08 09; do
    infile="cosmic_svafotate_ov${x}"
    outfile="cosmic-svafotate-ov${x}-popfreqs.txt"
    tail -n +2 ${!infile} | cut -f2 | sort -gr > $outfile
done

# extract popfreq column for needlr files
for x in 05 07 09; do
    infile="cosmic_needlr_ov${x}"
    outfile="cosmic-needlr-ov${x}-popfreqs.txt"
    tail -n +2 ${!infile} | cut -f2 | sed "s/$NEEDLR_FILTERED_SV_VALUE/0/" | sort -gr > $outfile
done

# plot density distributions
python $script \
    --figsize 6 5 \
    --inputs "cosmic-stix_lr-min_read1-popfreqs.txt,cosmic-stix_lr-min_read5-popfreqs.txt,cosmic-svafotate-ov05-popfreqs.txt,cosmic-svafotate-ov06-popfreqs.txt,cosmic-svafotate-ov07-popfreqs.txt,cosmic-svafotate-ov08-popfreqs.txt,cosmic-svafotate-ov09-popfreqs.txt,cosmic-needlr-ov05-popfreqs.txt,cosmic-needlr-ov07-popfreqs.txt,cosmic-needlr-ov09-popfreqs.txt" \
    --names "STIX-LR;MR=1,STIX-LR;MR=5,SVAFotate;OV=0.5,SVAFotate;OV=0.6,SVAFotate;OV=0.7,SVAFotate;OV=0.8,SVAFotate;OV=0.9,NeedLR;OV=0.5,NeedLR;OV=0.7,NeedLR;OV=0.9" \
    --near_zero_upper 0.01 \
    --output_near_zero_fractions "cosmic-sv-popfreq-near-zero-fractions.tsv" \
    --output_nonzero_fractions "cosmic-sv-popfreq-nonzero-fractions.tsv" \
    --xlabel "" \
    --ylabel_density "Population frequency > 0" \
    --output "cosmic-sv-popfreq-density.png" \
    --show_median







