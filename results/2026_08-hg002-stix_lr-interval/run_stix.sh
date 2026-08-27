#!/usr/bin/env bash

CPUS=10
INPUT=$(realpath hg002-stix_queries.tsv)
export FILE_LIMIT=65535
export INDEX="/data/jake/stix-lr-grch38"
export SHARDFILE=$INDEX/shardfile.txt
export SLOP=500
export OUTDIR=$(realpath output)
export ALT_FILE_COL=5
mkdir -p $OUTDIR
# ! conda activate giggle-dev

min_reads=(1 5)
for mr in "${min_reads[@]}"; do
	cat $INPUT |
		gargs -p $CPUS --log=run_stix.log \
			"ulimit -n ${FILE_LIMIT}; cd ${INDEX}; stix -c $ALT_FILE_COL -i $INDEX -P 500 -B $SHARDFILE -T $mr -l {1}:{2}-{3} -r {4}:{5}-{6} -t {7} > $OUTDIR/{0}.stix"
done

