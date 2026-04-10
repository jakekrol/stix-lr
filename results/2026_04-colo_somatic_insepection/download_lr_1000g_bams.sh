mkdir -p bams_lr_1000g

url_prefix="https://s3.amazonaws.com/1000g-ont/PROCESSED_DATA/ALIGNED_TO_HG38/MINIMAP2_ALIGNED_BAMS/"
url_suffix="-ONT-hg38-R9-LSK110-guppy-sup-5mC.phased.bam"
data=$(realpath "stix-lr-1000g-colo-somatic-samples.tsv")

pad=100000

cd bams_lr_1000g
while IFS=$'\t' read -r id sample reads chrom left_start left_end right_start right_end svtype svlen; do
    right=$((left_end + svlen))
    left_pad=$((left_start - pad))
    right_pad=$((right_end + pad))
    region="chr${chrom}:${left_pad}-${right_pad}"
    # get bai
    wget "${url_prefix}${sample}${url_suffix}.bai" -O "${sample}.bam.bai"
    # get bam
    url_bam="${url_prefix}${sample}${url_suffix}"
    echo "# downloading ${url_bam} for sample ${sample}"
    echo "# region: ${region}"
    samtools view \
        -b -o "${sample}.bam" \
        "${url_bam}" \
        "${region}"
done < <(tail -n +2 "$data")

# # test
# sample="GM18856"
# left=236097142
# length=11260
# right=$((left + length))
# left_pad=$((left - pad))
# right_pad=$((right + pad))
# chrom=1
# region="chr${chrom}:${left_pad}-${right_pad}"
# # get bai
# cd bams_lr_1000g
# wget "${url_prefix}${sample}${url_suffix}.bai" -O "${sample}.bam.bai"
# url_bam="${url_prefix}${sample}${url_suffix}"
# echo "# downloading ${url_bam}"
# echo "# region: ${region}"
# samtools view \
#     -b -o ${sample}.bam \
#     "${url_bam}" \
#     "${region}"
