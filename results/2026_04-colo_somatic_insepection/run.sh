#!/usr/bin/env bash

colo_somatic_counts=../2025_12-colo-stix_lr-filtered/stixlr.colo_somatic.min_read_5.svid_sample_counts.txt
vcf_in=../2025_12-colo-filtered/colo829_somatic_grch38_nogt00.vcf
index="/data/jake/stix-lr-grch38"
dirout=$(pwd)


echo "# finding colo somatic svs with non-zero sample counts"
awk 'NR == 1 {print; next} $2 > 0 {print}' $colo_somatic_counts > colo_somatic_non_zero.tsv

tail -n +2 colo_somatic_non_zero.tsv | cut -f 1 > colo_somatic_non_zero_ids.txt

echo "# filtering VCF for non-zero sample count IDs"
bcftools view --include 'ID=@colo_somatic_non_zero_ids.txt' "$vcf_in" -o colo_somatic_non_zero.vcf -O v

# vcf2stix query table
printf "ID\tCHROM\tPOS\tSVLEN\tALT\n" > colo_somatic_non_zero.stix_query.tsv
bcftools query -f '%ID\t%CHROM\t%POS\t[%SVLEN]\t%ALT\n' colo_somatic_non_zero.vcf \
    >> colo_somatic_non_zero.stix_query.tsv
./make_insertion_stix_queries.py \
    --input colo_somatic_non_zero.stix_query.tsv \
    --output colo_somatic_non_zero.stix_query.tsv

echo "# stix query for sample depths"
echo "# index: $index"
echo "# out directory: $dirout"
input=$(realpath "colo_somatic_non_zero.stix_query.tsv")
logfile=$(realpath "stix_lr_colo_somatic_non_zero.log")
(
    cd "$index" || { echo "Error: Could not change to directory $index"; exit 1; }
    tail -n +2 $input | \
        gargs -p 3 --log=$logfile \
            "stix -t {6} -B shardfile.txt -s 500 -c 5 -D -L {7} -l {1}:{2}-{3} -r {1}:{4}-{5}  > $dirout/{8}"
)

# extract depths
mapfile -t depthfiles < <(ls *.stix.depths)
for d in "${depthfiles[@]}"; do
    cut -f 6- $d | tr '\t' '\n' | sort -nr > $d.hist
done

# github.com/jakekrol/rl-tools/plot/hist.py
for d in "${depthfiles[@]}"; do
    svid="$(echo $d | cut -f 1 -d'.')"
    echo "$svid"
    cat $d.hist | \
        hist.py -o $d.hist.png --bins 10 --xlabel "Sample depth" --ylabel "Frequency" \
            --title "$svid" --ylog
done

# query again, but not the sample depth

echo "# stix query for non-depth info"
sed 's|\.depths||' colo_somatic_non_zero.stix_query.tsv > colo_somatic_non_zero.stix_query_no_depth.query.tsv
logfile=$(realpath "stix_lr_colo_somatic_non_zero_no_depth.log")
input=$(realpath "colo_somatic_non_zero.stix_query_no_depth.query.tsv")
(
    cd "$index" || { echo "Error: Could not change to directory $index"; exit 1; }
    tail -n +2 $input | \
        gargs -p 3 --log=$logfile \
            "stix -t {6} -B shardfile.txt -s 500 -c 5 -L {7} -l {1}:{2}-{3} -r {1}:{4}-{5}  > $dirout/{8}"
)

# get top 3 1000G samples with highest depth
mapfile -t stixfiles < <(ls *.stix)
for f in "${stixfiles[@]}"; do
    svid="$(echo $f | cut -f 1 -d'.')"
    grep "1000g" $f | \
        sort -k8 -nr | \
        head -n 3 > $svid.top_1000g_samples.tsv
done
