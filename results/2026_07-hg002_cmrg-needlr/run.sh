#!/usr/bin/env bash
# ! conda activate needLR-4.0-cyvcf2 before running
# ! make sure to use needLR fork

OVERLAPS=(0.5 0.7 0.9)
SCRIPT_GET_POP_FREQ=/data/jake/needLR-fork/src/annotate_collapsed_variants.py
OUTFILE_POPFREQ="needlr_pop_freq.tsv"
VCF_IN=../../data/2025_12-hg002-cmrg/HG002_GRCh38_difficult_medical_gene_SV_benchmark_v0.01_trusted_SVTYPE.addID.svafotate.AF.END.vcf.gz
cp $VCF_IN $(pwd)

for overlap in "${OVERLAPS[@]}"; do
    DIR_NEEDLR_OUT=needLR_ov${overlap}
    OUT_TIME=needLR_ov${overlap}.time.txt
    mkdir -p $DIR_NEEDLR_OUT
    echo "# needLR with truvari overlap ${overlap} to outdir $DIR_NEEDLR_OUT"
    t_0=$(date +%s)
    needLR annotate -O $DIR_NEEDLR_OUT -o $overlap $VCF_IN
    t_1=$(date +%s)
    echo "$((t_1-t_0)) seconds" > $OUT_TIME
    $SCRIPT_GET_POP_FREQ \
        --input_vcf "$VCF_IN" \
        --collapsed_vcf "$DIR_NEEDLR_OUT/*/*_truvari_collapsed_variants.vcf" \
        --table $DIR_NEEDLR_OUT/*/*RESULTS.tsv \
        --out "$DIR_NEEDLR_OUT/$OUTFILE_POPFREQ"
done




