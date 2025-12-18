#!/usr/bin/env bash

echo "DEPRECATED: use stix_lr-colo-parallel_contig.sh for parallelized version"
exit 1
srcdir=$(pwd)
colo_somatic="${srcdir}/../data/2025_11-colo_sv_calls/colo829_benchmark_grch38.vcf"
colo_germline="${srcdir}/../data/2025_11-colo_sv_calls/colo829_merge_grch38.vcf.gz"
outdir="${srcdir}/../results/2025_12-colo-stix_lr"
index="/data/jake/stix-lr-grch38"

cd $index || { echo "Error: Could not change to directory $index"; exit 1; }

echo "# somatic"

t=$(date +%s)
min_reads=5
echo "# running stix lr colo somatic with min reads: $min_reads"
outfile="${outdir}/colo_somatic.stix_lr.min_read_5.vcf"
if [ -f "$outfile" ]; then
    echo "# output file $outfile already exists, skipping..."
fi
stix -B shardfile.txt -s 500 -f $colo_somatic -T $min_reads > $outfile
echo "# completed in $(( $(date +%s) - t )) seconds"

min_reads=1
t=$(date +%s)
echo "# running stix lr colo somatic with min reads: $min_reads"
outfile="${outdir}/colo_somatic.stix_lr.min_read_1.vcf"
if [ -f "$outfile" ]; then
    echo "# output file $outfile already exists, skipping..."
fi
stix -B shardfile.txt -s 500 -f $colo_somatic -T $min_reads > $outfile
echo "# completed in $(( $(date +%s) - t )) seconds"

echo "# germline"

t=$(date +%s)
min_reads=5
echo "# running stix lr colo germline with min reads: $min_reads"
outfile="${outdir}/colo_germline.stix_lr.min_read_5.vcf"
if [ -f "$outfile" ]; then
    echo "# output file $outfile already exists, skipping..."
fi
stix -B shardfile.txt -s 500 -f $colo_germline -T $min_reads > $outfile
echo "# completed in $(( $(date +%s) - t )) seconds"

min_reads=1
t=$(date +%s)
echo "# running stix lr colo germline with min reads: $min_reads"
outfile="${outdir}/colo_germline.stix_lr.min_read_1.vcf"
if [ -f "$outfile" ]; then
    echo "# output file $outfile already exists, skipping..."
fi
stix -B shardfile.txt -s 500 -f $colo_germline -T $min_reads > $outfile
echo "# completed in $(( $(date +%s) - t )) seconds"

echo "# all done"
