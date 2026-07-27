#!/usr/bin/env bash

# conda activate needLR-4.0 before running

CPUS=50
OUTDIR='out'
mkdir -p in_vcfs
cp ../2026-07-split_vcfs_for_needlr/hg002_cmrg_split/* in_vcfs/
ls in_vcfs > vcfs.txt
(
    cd in_vcfs
    cat ../vcfs.txt | gargs -p $CPUS "bgzip -c {0} > {0}.gz"
)
sed -i "s|$|.gz|" vcfs.txt
sed "s|.vcf||" vcfs.txt > outdirs.txt
sed -i "s|^|$OUTDIR/|" outdirs.txt
cat outdirs.txt | gargs -p $CPUS "mkdir -p {0}"
sed -i "s|^|in_vcfs/|" vcfs.txt
paste vcfs.txt outdirs.txt > gargs.input
t_0=$(date +%s)
cat gargs.input | \
    gargs \
        --log=gargs.log \
        -p $CPUS \
        "needLR annotate -O {1} {0}"
t_1=$(date +%s)
# write time
echo "Time taken: $((t_1 - t_0)) seconds" > gargs.time

