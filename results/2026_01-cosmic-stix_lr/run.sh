#!/usr/bin/env bash

POPSIZE=1108

outdir=$(pwd)
vcf="${outdir}/../2026_01-cosmic-tsv-to-vcf/cosmic.v103.grch38.vcf"
index="/data/jake/stix-lr-grch38"
timefile="${outdir}/stix_lr_cosmic.times"
if [ -f "$timefile" ]; then
    echo "# timefile $timefile already exists, exiting to avoid overwriting"
    exit 1
fi


cd $index || { echo "Error: Could not change to directory $index"; exit 1; }

min_reads=5
echo "# running stix lr cosmic with min reads: $min_reads"
outfile="${outdir}/cosmic.stix_lr.min_read_5.vcf"
if [ -f "$outfile" ]; then
    echo "# output file $outfile already exists, exiting to avoid overwriting"
    exit 1
fi
t_s=$(date +%s)
stix -B shardfile.txt -s 500 -f $vcf -T $min_reads > $outfile
t_e=$(date +%s)
t_diff=$(( t_e - t_s ))
printf "cosmic.stix_lr.min_read_5\t%s\n" "$t_diff" >> $timefile
echo "# completed in $t_diff seconds"

min_reads=1
echo "# running stix lr cosmic with min reads: $min_reads"
outfile="${outdir}/cosmic.stix_lr.min_read_1.vcf"
if [ -f "$outfile" ]; then
    echo "# output file $outfile already exists, exiting to avoid overwriting"
    exit 1
fi
t_s=$(date +%s)
stix -B shardfile.txt -s 500 -f $vcf -T $min_reads > $outfile
t_e=$(date +%s)
t_diff=$(( t_e - t_s ))
printf "cosmic.stix_lr.min_read_1\t%s\n" "$t_diff" >> $timefile
echo "# completed in $t_diff seconds"

# extract sample counts and pop freq for each variant
mrs=(1 5)
script="../../src/stixlr_vcfout2svid_cample_count.py"
for mr in "${mrs[@]}"; do
    infile="${outdir}/cosmic.stix_lr.min_read_${mr}.vcf"
    outfile="${outdir}/cosmic.stix_lr.min_read_${mr}.tsv"
    if [ -f "$outfile" ]; then
        echo "# output file $outfile already exists, skipping"
        continue
    fi
    echo "# extracting sample counts for min read $mr"
    $script -i $infile -o $outfile --add_header
done

# sample counts to population frequencies
for mr in "${mrs[@]}"; do
    infile="${outdir}/cosmic.stix_lr.min_read_${mr}.tsv"
    outfile="${outdir}/cosmic.stix_lr.min_read_${mr}.popfreq.tsv"
    # if [ -f "$outfile" ]; then
    #     echo "# output file $outfile already exists, skipping"
    #     continue
    # fi
    echo "# converting sample counts to population frequencies for min read $mr"
    printf "svid\tpop_freq\n" > "$outfile"
    tail -n +2 "$infile" | \
        awk -F'\t' -v OFS='\t' -v ps=$POPSIZE 'NR==1 {print; next} {$2=$2/ps; print}' | \
        sort -k2 -rn >> "$outfile"
done


