#!/usr/bin/env bash
# activate conda needlr env before running
# set -euo pipefail
t_0=$(date +%s)

# paths
export TMPDIR=/data/jake/tmp
TIMEFILE=$(realpath ./needLR_run_time.tsv)
# ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz
# bgzip and index with samtools faidx
NEEDLR_GRCH38_REFERENCE=/data/jake/needLR/needLR_v3.5_local/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz
# dir of needlr install
dirneedlr="/data/jake/needLR/needLR_v3.5_local"
OUTDIR=$(pwd)
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

# colo svs
echo "# finding colo829 vcfs"
somatic=../2025_12-colo-filtered/colo829_somatic_grch38_nogt00.vcf
germline=../2025_12-colo-filtered/colo829_germline.vcf
cp $somatic $germline $OUTDIR
somatic=$(basename $somatic)
germline=$(basename $germline)

# fix header, bgzip, and index
echo "# fixing VCF headers, bgzipping and indexing vcfs"
for f in $germline $somatic; do
    # rm BND
    grep -v 'SVTYPE=BND' $f > temp.vcf && mv temp.vcf $f
    # Add AF field and fix END type from String to Integer
    sed -i '32i##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">' $f
    sed -i 's/ID=END,Number=1,Type=String/ID=END,Number=1,Type=Integer/' $f
    bgzip -f $f
    tabix -f ${f}.gz
done
# run needlr
for f in $germline $somatic; do
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
    mv $dirneedlr/needLR_output/* $OUTDIR
    printf "$f\t$run_time\n" >> $TIMEFILE
    # go back to origin dir
    cd $DIRORIGIN || { echo "Could not change to origin directory $DIRORIGIN"; exit 1; }
done

t_1=$(date +%s)
t_total=$((t_1 - t_0))
echo "# done. total time $t_total seconds"

# echo "# preparing needLR input file"
# # write input file
# somatic=$(realpath ${somatic}.gz)
# germline=$(realpath ${germline}.gz)
# # printf "$somatic\n$germline\n" > input_vcfs.txt
# printf "$somatic\n" > input_vcfs.txt
# inputfile=$(realpath input_vcfs.txt)

# # change to needlr dir for running
# cd $dirneedlr || { echo "Could not change to needlr directory $dirneedlr"; exit 1; }

# # run needlr
# echo "# running needLR on $inputfile"
# ./needLR_v3.5_basic.sh -g $NEEDLR_GRCH38_REFERENCE -l $inputfile

# t_1=$(date +%s)
# total_time=$((t_1 - t_0))
# echo "# needLR run completed in $total_time seconds"
