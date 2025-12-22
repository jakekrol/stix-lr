#!/usr/bin/env bash
set -euo pipefail
t_0=$(date +%s)
export TMPDIR=$1
tmp=$(mktemp -d $TMPDIR/tar_colo.XXXXXX)
trap 'rm -rf $TMPDIR/tar_colo.*' EXIT

# do realpath mapping for each file
stix_lr=(
    "$(realpath ../2025_12-colo-stix_lr-filtered/stixlr.colo_germline.min_read_1.svid_sample_counts.txt)"
    "$(realpath ../2025_12-colo-stix_lr-filtered/stixlr.colo_germline.min_read_5.svid_sample_counts.txt)"
    "$(realpath ../2025_12-colo-stix_lr-filtered/stixlr.colo_somatic.min_read_1.svid_sample_counts.txt)"
    "$(realpath ../2025_12-colo-stix_lr-filtered/stixlr.colo_somatic.min_read_5.svid_sample_counts.txt)"
)
svafotate=(
    "$(realpath ../2025_12-colo-svafotate-filtered/svafotate.colo_germline.svid_popfreq.ov0.5.txt)"
    "$(realpath ../2025_12-colo-svafotate-filtered/svafotate.colo_germline.svid_popfreq.ov0.6.txt)"
    "$(realpath ../2025_12-colo-svafotate-filtered/svafotate.colo_germline.svid_popfreq.ov0.7.txt)"
    "$(realpath ../2025_12-colo-svafotate-filtered/svafotate.colo_germline.svid_popfreq.ov0.8.txt)"
    "$(realpath ../2025_12-colo-svafotate-filtered/svafotate.colo_germline.svid_popfreq.ov0.9.txt)"
    "$(realpath ../2025_12-colo-svafotate-filtered/svafotate.colo_somatic.svid_popfreq.ov0.5.txt)"
    "$(realpath ../2025_12-colo-svafotate-filtered/svafotate.colo_somatic.svid_popfreq.ov0.6.txt)"
    "$(realpath ../2025_12-colo-svafotate-filtered/svafotate.colo_somatic.svid_popfreq.ov0.7.txt)"
    "$(realpath ../2025_12-colo-svafotate-filtered/svafotate.colo_somatic.svid_popfreq.ov0.8.txt)"
    "$(realpath ../2025_12-colo-svafotate-filtered/svafotate.colo_somatic.svid_popfreq.ov0.9.txt)"
)

echo "# creating tarball of hg002 cmrg stix lr and svafotate results in $tmp"
(
    cd  $tmp 
    cp "${stix_lr[@]}" .
    cp "${svafotate[@]}" .
    tar -czvf colo_filtered_stix_lr_svafotate_results.tar.gz ./*
)
mv $tmp/colo_filtered_stix_lr_svafotate_results.tar.gz .
echo "# tarball created at ./colo_filtered_stix_lr_svafotate_results.tar.gz"
echo "# elapsed time: $(( $(date +%s) - t_0 )) seconds"