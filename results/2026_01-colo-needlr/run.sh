#!/usr/bin/env bash
set -euo pipefail
t_0=$(date +%s)
# ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz
NEEDLR_GRCH38_REFERENCE=/data/jake/needLR/needLR_v3.5_local/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz
# dir of needlr install
dirneedlr="/data/jake/needLR/needLR_v3.5_local"


# colo svs
echo "# finding colo829 vcfs"
somatic=../2025_12-colo-filtered/colo829_somatic_grch38_nogt00.vcf
germline=../2025_12-colo-filtered/colo829_germline.vcf
cp $somatic $germline .
somatic=$(basename $somatic)
germline=$(basename $germline)

# fix header, bgzip, and index
echo "# fixing VCF headers, bgzipping and indexing vcfs"
for f in $somatic $germline; do
    # rm BND
    grep -v 'SVTYPE=BND' $f > temp.vcf && mv temp.vcf $f
    # Add AF field and fix END type from String to Integer
    sed -i '32i##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">' $f
    sed -i 's/ID=END,Number=1,Type=String/ID=END,Number=1,Type=Integer/' $f
    bgzip -f $f
    tabix -f ${f}.gz
done

# clean up any previous runs
rm -rfi "$dirneedlr/needLR_output/colo829_somatic_grch38_nogt00_needLR_v3.5_basic"

echo "# preparing needLR input file"
# write input file
somatic=$(realpath ${somatic}.gz)
germline=$(realpath ${germline}.gz)
# printf "$somatic\n$germline\n" > input_vcfs.txt
printf "$somatic\n" > input_vcfs.txt
inputfile=$(realpath input_vcfs.txt)

# change to needlr dir for running
cd $dirneedlr || { echo "Could not change to needlr directory $dirneedlr"; exit 1; }

# run needlr
echo "# running needLR on $inputfile"
./needLR_v3.5_basic.sh -g $NEEDLR_GRCH38_REFERENCE -l $inputfile

t_1=$(date +%s)
total_time=$((t_1 - t_0))
echo "# needLR run completed in $total_time seconds"
