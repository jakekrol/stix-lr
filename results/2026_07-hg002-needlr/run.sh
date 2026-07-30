#!/usr/bin/env bash
# ! conda activate needLR-4.0-cyvcf2 before running
# ! make sure to use needLR fork

OVERLAPS=(0.5 0.7 0.9)
SCRIPT_GET_POP_FREQ=/data/jake/needLR-fork/src/annotate_collapsed_variants.py
OUTFILE_POPFREQ="needlr_pop_freq.tsv"
VCF_IN=../../data/2026_07-hg002-svs/GRCh38_HG002-T2TQ100-V1.0_stvar.AF.addID.vcf.gz
cp $VCF_IN $(pwd) # not necessary
# needLR names outdirs based on input vcf name
DIR_NEEDLR_OUT=$(basename $VCF_IN)
DIR_NEEDLR_OUT="${DIR_NEEDLR_OUT%.vcf.gz}_needLR_1kg_v4.0"

for overlap in "${OVERLAPS[@]}"; do
    dir_overlap_out="needLR_ov${overlap}"
    mkdir -p ${dir_overlap_out}
    out_time=needLR_ov${overlap}.time.txt
    dir_out="${dir_overlap_out}/${DIR_NEEDLR_OUT}"

    echo "# needLR with truvari overlap ${overlap} to outdir ${dir_overlap_out}"
    t_0=$(date +%s)
    needLR annotate -O ${dir_overlap_out} -o ${overlap} ${VCF_IN}
    t_1=$(date +%s)
    echo "$((t_1-t_0)) seconds" > ${out_time}

    collapsed_vcf=$(find ${dir_out} -type f -iname "*_truvari_collapsed_variants.vcf")
    needlr_table=$(find ${dir_out} -type f -iname "*RESULTS.tsv")
    ${SCRIPT_GET_POP_FREQ} \
        --input_vcf "${VCF_IN}" \
        --collapsed_vcf "${collapsed_vcf}" \
        --table "${needlr_table}" \
        --out "${dir_overlap_out}/${OUTFILE_POPFREQ}"
done




