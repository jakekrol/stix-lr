#!/usr/bin/env bash

# ! conda activate giggle-dev
CPUS=15
INPUT=$(realpath hg002-stix_queries.tsv)
export FILE_LIMIT=65535
echo "# FILE_LIMIT=${FILE_LIMIT}"
export INDEX="/data/jake/stix-lr-grch38"
echo "# INDEX=${INDEX}"
export SHARDFILE=$INDEX/shardfile.txt
echo "# SHARDFILE=${SHARDFILE}"
export SLOP=500
echo "# SLOP=${SLOP}"
export OUTDIR_PATTERN=$(realpath output-)
echo "# OUTDIR_PATTERN=${OUTDIR_PATTERN}"
export ALT_FILE_COL=5
echo "# ALT_FILE_COL=${ALT_FILE_COL}"
TIMEFILE=hg002-stixlr.times
echo "# TIMEFILE=${TIMEFILE}"

if [ -f "$TIMEFILE" ]; then
    echo "# timefile $TIMEFILE already exists, exiting to avoid overwriting"
    exit 1
fi
printf "tool\tseconds\n" >> $TIMEFILE

min_reads=(1 5)
for mr in "${min_reads[@]}"; do
	OUTDIR=${OUTDIR_PATTERN}mr_${mr}
	mkdir -p $OUTDIR
	t_s=$(date +%s)
	cat $INPUT |
		gargs -p $CPUS --log=run_stix.log \
			"ulimit -n ${FILE_LIMIT}; cd ${INDEX}; stix -c $ALT_FILE_COL -i $INDEX -P $SLOP -B $SHARDFILE -T $mr -l {1}:{2}-{3} -r {4}:{5}-{6} -t {7} > $OUTDIR/{0}.stix"
	t_e=$(date +%s)
	t_diff=$(( t_e - t_s ))
	printf "stixlr_mr${mr}\t$t_diff\n" >> $TIMEFILE
done

