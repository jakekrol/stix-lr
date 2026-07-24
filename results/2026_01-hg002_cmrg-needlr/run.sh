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

# hg002 svs
echo "# finding hg002 vcfs"
hg002cmrgvcf="../../data/2025_12-hg002-cmrg/HG002_GRCh38_difficult_medical_gene_SV_benchmark_v0.01_trusted_SVTYPE.addID.svafotate.vcf"
cp $hg002cmrgvcf $DIRORIGIN
hg002cmrgvcf=$(basename $hg002cmrgvcf)

# bgzip and index
echo "# fixing VCF headers, bgzipping and indexing vcfs"
for f in $hg002cmrgvcf; do
    bgzip -f $f
    tabix -f ${f}.gz
done
# run needlr
for f in $hg002cmrgvcf; do
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
tail -n +2 $f | cut -f $NEEDLR_POPFREQ_COL > hg002_needlr_popfreqs.txt
sort -gn hg002_needlr_popfreqs.txt > xyz && mv xyz hg002_needlr_popfreqs.txt

n_svs=$(wc -l hg002_needlr_popfreqs.txt | cut -d' ' -f1)
script='n_pop_freq_non_zero_svs=0
with open("hg002_needlr_popfreqs.txt") as f:
    for line in f:
        if float(line.strip()) > 0.0:
            n_pop_freq_non_zero_svs += 1
print(n_pop_freq_non_zero_svs)
'
n_svs_non_zero_pop_freq=$(python3 -c "$script")
recall=$(calc $n_svs_non_zero_pop_freq / $n_svs)
recall=$(calc ${recall}*100)
recall=$(echo "${recall} %")
echo "$recall" > hg002_needlr_recall.txt

# bed
../../src/needlrout2bed.py -i $f -o hg002_cmrg_needlr_popfreqs.bed
mkdir -p bed_in bed_out
mv hg002_cmrg_needlr_popfreqs.bed bed_in
../../src/sort_bed bed_in bed_out 4
gunzip -c bed_out/hg002_cmrg_needlr_popfreqs.bed.gz > hg002_cmrg_needlr_popfreqs.bed

t_1=$(date +%s)
t_total=$((t_1 - t_0))
echo "# done. total time $t_total seconds"

