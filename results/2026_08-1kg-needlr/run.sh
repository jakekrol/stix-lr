#!/usr/bin/env bash
# ! conda activate needLR-4.0-cyvcf2 before running
# ! make sure to use needLR fork
# ! source jkbiolib

OVERLAPS=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
export OVERLAPS
SCRIPT_GET_POP_FREQ=/data/jake/needLR-fork/src/annotate_collapsed_variants.py
export SCRIPT_GET_POP_FREQ
OUTFILE_POPFREQ="needlr_pop_freq.tsv"
export OUTFILE_POPFREQ
VCF_IN=../../data/2026_08-thousg_svs/1KGP_3202.gatksv_svtools_novelins.freeze_V3.wAF.vcf.gz
export VCF_IN
# needLR names outdirs based on input vcf name
DIR_NEEDLR_OUT=$(basename $VCF_IN)
DIR_NEEDLR_OUT="${DIR_NEEDLR_OUT%.vcf.gz}_needLR_1kg_v4.0"
export DIR_NEEDLR_OUT
cp $VCF_IN $(pwd) # not necessary
GARGS_INPUT=input.tsv

run_needlr () {
    local overlap=$1
    local outdir=$2
    local outdir_needlr=$3
    local outtime=$4
    echo "# needLR with truvari overlap ${overlap} to outdir ${outdir}"
    t_0=$(date +%s)
    needLR annotate -O ${outdir} -o ${overlap} ${VCF_IN}
    t_1=$(date +%s)
    echo "$((t_1-t_0)) seconds" > ${outtime}
    collapsed_vcf=$(find ${outdir_needlr} -type f -iname "*_truvari_collapsed_variants.vcf")
    merged_vcf=$(find ${outdir_needlr} -type f -iname "*_truvari_collapse_out.vcf")
    echo "# annotating needlr popfreqs with truvari overlap ${overlap} to outdir ${outdir}"
    ${SCRIPT_GET_POP_FREQ} \
        --input_vcf "${VCF_IN}" \
        --collapsed_vcf "${collapsed_vcf}" \
        --merged_vcf "${merged_vcf}" \
        --out "${outdir}/${OUTFILE_POPFREQ}"
}
export -f run_needlr


rm ${GARGS_INPUT} || echo "# no previous ${GARGS_INPUT} file to remove"
echo "# constructing gargs parallel file: ${GARGS_INPUT}"
for overlap in "${OVERLAPS[@]}"; do
    dir_overlap_out="needLR_ov${overlap}"
    mkdir -p ${dir_overlap_out}
    out_time=needLR_ov${overlap}.time.txt
    dir_out="${dir_overlap_out}/${DIR_NEEDLR_OUT}"
    printf "%s\t%s\t%s\t%s\n" "${overlap}" "${dir_overlap_out}" "${dir_out}" "${out_time}" >> ${GARGS_INPUT}
done

# source bashrc for conda init
cat $GARGS_INPUT | \
    gargs -p 9 --log=gargs.log "source ~/.bashrc; conda activate needLR-4.0-cyvcf2; source /data/jake/jkbiolib/.venv/bin/activate; run_needlr {0} {1} {2} {3}"
