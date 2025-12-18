#!/usr/bin/env bash
# /data/jake/tmp
set -euo pipefail
t_0=$(date +%s)
outdir='../results/2025_12-hg002_all'
mkdir -p $outdir
export TMPDIR=$1
tmp=$(mktemp -d $TMPDIR/tar_hg002.XXXXXX)
trap 'rm -rf $TMPDIR/tar_hg002.*' EXIT

# do realpath mapping for each file
stix_lr=(
    "$(realpath ../results/2025_12-hg002_cmrg-stix_lr/hg002_cmrg.stix_lr.min_read_1.popfreq.tsv)"
    "$(realpath ../results/2025_12-hg002_cmrg-stix_lr/hg002_cmrg.stix_lr.min_read_5.popfreq.tsv)"
)
svafotate=(
    "$(realpath ../results/2025_12-hg002_cmrg-svafotate/svafotate-hg002-cmrg-overlap_0.5_maxpopfreq.txt)"
    "$(realpath ../results/2025_12-hg002_cmrg-svafotate/svafotate-hg002-cmrg-overlap_0.6_maxpopfreq.txt)"
    "$(realpath ../results/2025_12-hg002_cmrg-svafotate/svafotate-hg002-cmrg-overlap_0.7_maxpopfreq.txt)"
    "$(realpath ../results/2025_12-hg002_cmrg-svafotate/svafotate-hg002-cmrg-overlap_0.8_maxpopfreq.txt)"
    "$(realpath ../results/2025_12-hg002_cmrg-svafotate/svafotate-hg002-cmrg-overlap_0.9_maxpopfreq.txt)"
)

echo "# creating tarball of hg002 cmrg stix lr and svafotate results in $tmp"
(
    cd  $tmp 
    cp "${stix_lr[@]}" .
    cp "${svafotate[@]}" .
    tar -czvf hg002_cmrg_stix_lr_svafotate_results.tar.gz ./*
)
mv $tmp/hg002_cmrg_stix_lr_svafotate_results.tar.gz $outdir
echo "# tarball created at $outdir/hg002_cmrg_stix_lr_svafotate_results.tar.gz"
echo "# elapsed time: $(( $(date +%s) - t_0 )) seconds"

