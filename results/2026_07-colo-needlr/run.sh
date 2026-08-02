#!/usr/bin/env bash
# ! conda activate needLR-4.0-cyvcf2 before running
# ! make sure to use needLR fork

OVERLAPS=(0.5 0.7 0.9)
SCRIPT_GET_POP_FREQ=/data/jake/needLR-fork/src/annotate_collapsed_variants.py
OUTFILE_POPFREQ="needlr_pop_freq.tsv"
vcf_somatic=../2025_12-colo-filtered/colo829_somatic_grch38_nogt00.vcf
vcf_germline=../2025_12-colo-filtered/colo829_germline.vcf
# needLR names outdirs based on input vcf name

for vcf in $vcf_somatic $vcf_germline; do
    cp $vcf $(pwd)
    vcf=$(basename $vcf)
    echo "# fixing VCF headers, bgzipping and indexing $vcf"
    # Add AF field and fix END type from String to Integer
    sed -i '32i##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">' $vcf
    sed -i 's/ID=END,Number=1,Type=String/ID=END,Number=1,Type=Integer/' $vcf
    bgzip -f $vcf
    tabix -f ${vcf}.gz
    vcf=${vcf}.gz
done

vcf_somatic=$(basename ${vcf_somatic}.gz)
vcf_germline=$(basename ${vcf_germline}.gz)

### somatic
prefix="somatic"
for overlap in "${OVERLAPS[@]}"; do
    dir_overlap_out="${prefix}_needLR_ov${overlap}"
    mkdir -p ${dir_overlap_out}
    out_time=${prefix}_needLR_ov${overlap}.time.txt
    # needlr outdir name depends on input vcf
    dir_needlr_out=$(basename ${vcf_somatic})
    dir_needlr_out="${dir_needlr_out%.vcf.gz}_needLR_1kg_v4.0"
    dir_out="${dir_overlap_out}/${dir_needlr_out}"

    echo "# needLR with truvari overlap ${overlap} to outdir ${dir_overlap_out}"
    t_0=$(date +%s)
    needLR annotate -O ${dir_overlap_out} -o ${overlap} ${vcf_somatic}
    t_1=$(date +%s)
    echo "$((t_1-t_0)) seconds" > ${out_time}

    collapsed_vcf=$(find ${dir_out} -type f -iname "*_truvari_collapsed_variants.vcf")
    needlr_table=$(find ${dir_out} -type f -iname "*RESULTS.tsv")
    ${SCRIPT_GET_POP_FREQ} \
        --input_vcf "${vcf_somatic}" \
        --collapsed_vcf "${collapsed_vcf}" \
        --table "${needlr_table}" \
        --out "${dir_overlap_out}/${OUTFILE_POPFREQ}"
    unset collapsed_vcf
    unset needlr_table
done

### germline
prefix="germline"
for overlap in "${OVERLAPS[@]}"; do
    dir_overlap_out="${prefix}_needLR_ov${overlap}"
    mkdir -p ${dir_overlap_out}
    out_time=${prefix}_needLR_ov${overlap}.time.txt
    # needlr outdir name depends on input vcf
    dir_needlr_out=$(basename ${vcf_germline})
    dir_needlr_out="${dir_needlr_out%.vcf.gz}_needLR_1kg_v4.0"
    dir_out="${dir_overlap_out}/${dir_needlr_out}"

    echo "# needLR with truvari overlap ${overlap} to outdir ${dir_overlap_out}"
    t_0=$(date +%s)
    needLR annotate -O ${dir_overlap_out} -o ${overlap} ${vcf_germline}
    t_1=$(date +%s)
    echo "$((t_1-t_0)) seconds" > ${out_time}

    collapsed_vcf=$(find ${dir_out} -type f -iname "*_truvari_collapsed_variants.vcf")
    needlr_table=$(find ${dir_out} -type f -iname "*RESULTS.tsv")
    ${SCRIPT_GET_POP_FREQ} \
        --input_vcf "${vcf_germline}" \
        --collapsed_vcf "${collapsed_vcf}" \
        --table "${needlr_table}" \
        --out "${dir_overlap_out}/${OUTFILE_POPFREQ}"
    unset collapsed_vcf
    unset needlr_table
done




