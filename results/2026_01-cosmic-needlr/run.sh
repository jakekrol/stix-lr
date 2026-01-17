#!/usr/bin/env bash
# activate conda needlr env before running
# set -euo pipefail
t_0=$(date +%s)
  
NEEDLR_POPFREQ_COL=43
# paths
export TMPDIR=/data/jake/tmp
TIMEFILE=$(realpath ./needLR_run_time.tsv)
# ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz
# bgzip and index with samtools faidx
NEEDLR_GRCH38_REFERENCE=/data/jake/needLR/needLR_v3.5_local/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz
# dir of needlr install
dirneedlr="/data/jake/needLR/needLR_v3.5_local"
OUTDIR="$(pwd)"/needlr_out-$(date +%Y%m%d_%H%M%S)
mkdir -p $OUTDIR
DIRORIGIN=$(pwd)
# echo all the paths
echo "# TMPDIR: $TMPDIR"
echo "# NEEDLR_GRCH38_REFERENCE: $NEEDLR_GRCH38_REFERENCE"
echo "# needlr dir: $dirneedlr"
echo "# output dir: $OUTDIR"
echo "# origin dir: $DIRORIGIN"
echo "# time file: $TIMEFILE"


if [[ -f $TIMEFILE ]]; then
    echo "# removing previous time file $TIMEFILE"
    rm -f $TIMEFILE
fi

# cosmic svs
echo "# finding cosmic vcfs"
cosmicvcf="../2026_01-cosmic-tsv-to-vcf/cosmic.v103.grch38.vcf"
cp $cosmicvcf $DIRORIGIN
cosmicvcf=$(basename $cosmicvcf)

# bgzip and index
echo "# fixing VCF headers, bgzipping and indexing vcfs"
for f in $cosmicvcf; do
    bgzip -f $f
    tabix -f ${f}.gz
done
# run needlr
for f in $cosmicvcf; do
    # make required input file
    f=$(realpath ${f}.gz)
    inputfile=$(mktemp "${TMPDIR}/input_vcf_XXXX.txt")
    trap "rm -f $inputfile" EXIT
    printf "$f\n" > $inputfile
    # change to needlr dir for running
    cd $dirneedlr || { echo "Could not change to needlr directory $dirneedlr"; exit 1; }
    echo "# running needLR on $f"
    # time needlr run
    t_s=$(date +%s)
    ./needLR_v3.5_basic.sh -g $NEEDLR_GRCH38_REFERENCE -l $inputfile
    t_e=$(date +%s)
    run_time=$((t_e - t_s))
    # move result
    mv --no-clobber $dirneedlr/needLR_output/* $OUTDIR
    printf "$f\t$run_time\n" >> $TIMEFILE
    # go back to origin dir
    cd $DIRORIGIN || { echo "Could not change to origin directory $DIRORIGIN"; exit 1; }
done

f=$(find $OUTDIR -type f -name "*RESULTS.txt")
tail -n +2 $f | cut -f $NEEDLR_POPFREQ_COL > cosmic_needlr_popfreqs.txt

t_1=$(date +%s)
t_total=$((t_1 - t_0))
echo "# done. total time $t_total seconds"
