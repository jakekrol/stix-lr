#!/usr/bin/env bash
set -euo pipefail

# see github.com/jakekrol/rl-tools/plot/density.py
script=./density.py
# num samples in stix lr index to normalize counts in to frequencies
POPSIZE=1108

#### inputs

### stix lr
# dir_cosmic_stix=../2026_01-cosmic-stix_lr
# cosmic_stix_min_read1=$dir_cosmic_stix/cosmic.stix_lr.min_read_1.vcf
# cosmic_stix_min_read5=$dir_cosmic_stix/cosmic.stix_lr.min_read_5.vcf
### svafotate
dir_cosmic_svafotate=../2026_01-cosmic-svafotate
cosmic_svafotate_ov05=$dir_cosmic_svafotate/svafotate-cosmic_overlap_0.5_maxpopfreq.txt
cosmic_svafotate_ov06=$dir_cosmic_svafotate/svafotate-cosmic_overlap_0.6_maxpopfreq.txt
cosmic_svafotate_ov07=$dir_cosmic_svafotate/svafotate-cosmic_overlap_0.7_maxpopfreq.txt
cosmic_svafotate_ov08=$dir_cosmic_svafotate/svafotate-cosmic_overlap_0.8_maxpopfreq.txt
cosmic_svafotate_ov09=$dir_cosmic_svafotate/svafotate-cosmic_overlap_0.9_maxpopfreq.txt
### needlr
dir_cosmic_needlr=../2026_01-cosmic-needlr
cosmic_needlr=$dir_cosmic_needlr/cosmic_needlr_popfreqs.txt

# transform stix sample counts to population frequencies
# tail -n +2 $cosmic_stix_min_read1 | \
#     awk -v ps=$POPSIZE 'BEGIN{OFS="\t"} {print $2/ps}' | \
#     sort -nr > cosmic-stix_lr-min_read1-popfreqs.txt
# tail -n +2 $cosmic_stix_min_read5 | \
#     awk -v ps=$POPSIZE 'BEGIN{OFS="\t"} {print $2/ps}' | \
#     sort -nr > cosmic-stix_lr-min_read5-popfreqs.txt

# extract popfreq column for svafotate files
for x in 05 06 07 08 09; do
    infile="cosmic_svafotate_ov${x}"
    outfile="cosmic-svafotate-ov${x}-popfreqs.txt"
    tail -n +2 ${!infile} | cut -f2 | sort -gr > $outfile
done

# plot density distributions
python $script \
    --figsize 10 5 \
    --inputs "cosmic-svafotate-ov05-popfreqs.txt,cosmic-svafotate-ov06-popfreqs.txt,cosmic-svafotate-ov07-popfreqs.txt,cosmic-svafotate-ov08-popfreqs.txt,cosmic-svafotate-ov09-popfreqs.txt,$cosmic_needlr" \
    --names "SVAFotate;OV=0.5,SVAFotate;OV=0.6,SVAFotate;OV=0.7,SVAFotate;OV=0.8,SVAFotate;OV=0.9,NeedLR" \
    --title "COSMIC SV Population Frequency Distributions" \
    --xlabel "" \
    --ylabel "Population frequency" \
    --output "cosmic-sv-popfreq-density.png" \
    --threshold 0.2 \
    --debug
    # --names "STIX-LR;MR=1,STIX-LR;MR=5,SVAFotate;OV=0.5,SVAFotate;OV=0.6,SVAFotate;OV=0.7,SVAFotate;OV=0.8,SVAFotate;OV=0.9,NeedLR" \
    # --inputs "cosmic-stix_lr-min_read1-popfreqs.txt,cosmic-stix_lr-min_read5-popfreqs.txt,cosmic-svafotate-ov05-popfreqs.txt,cosmic-svafotate-ov06-popfreqs.txt,cosmic-svafotate-ov07-popfreqs.txt,cosmic-svafotate-ov08-popfreqs.txt,cosmic-svafotate-ov09-popfreqs.txt,$cosmic_needlr" \






