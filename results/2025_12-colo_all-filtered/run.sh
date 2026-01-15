#!/usr/bin/env bash
set -euo pipefail
t_0=$(date +%s)
export TMPDIR=$1
tmp=$(mktemp -d $TMPDIR/tar_colo.XXXXXX)
trap 'rm -rf $TMPDIR/tar_colo.*' EXIT
outfile="colo_filtered_stix_lr_svafotate_needlr_results.tar.gz"

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
    "$(realpath ../2026_01-colo-svafotate-filt-rerun/svafotate_germline.time)"
    "$(realpath ../2026_01-colo-svafotate-filt-rerun/svafotate_somatic.time)"
)
needlr=(
    "$(find ../2026_01-colo-needlr/ -type f -name "*RESULTS.txt" -path "*somatic*" -exec realpath {} \; | grep -v backup )"
    "$(find ../2026_01-colo-needlr/ -type f -name "*popfreqs.txt" -path "*somatic*" -exec realpath {} \; | grep -v backup )"
    "$(find ../2026_01-colo-needlr/ -type f -name "*RESULTS.txt" -path "*germline*" -exec realpath {} \; | grep -v backup )"
    "$(find ../2026_01-colo-needlr/ -type f -name "*popfreqs.txt" -path "*germline*" -exec realpath {} \; | grep -v backup )"
    "$(realpath ../2026_01-colo-needlr/needLR_run_time.tsv)"
)

echo "# creating tarball of colo stix lr svafotate and needlr results in $tmp"
(
    cd  $tmp 
    cp "${stix_lr[@]}" .
    cp "${svafotate[@]}" .
    cp "${needlr[@]}" .
    tar -czvf "$outfile" ./*
)
mv $tmp/"$outfile" .
echo "# tarball created at ./$outfile"
echo "# elapsed time: $(( $(date +%s) - t_0 )) seconds"