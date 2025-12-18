#!/usr/bin/env bash
t_0=$(date +%s)
set -euo pipefail

while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--input)
            input_vcf="$2"
            shift 2
            ;;
        -o|--outdir)
            outdir="$2"
            shift 2
            ;;
        --tempdir)
            temp_dir="$2"
            export TMPDIR="$temp_dir"
            shift 2
            ;;
        --prefix)
            prefix="$2"
            shift 2
            ;;
        --vcf_needs_bgz)
            vcf_needs_bgz=true
            shift 1
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done


# validation
if [[ -z "${input_vcf:-}" || -z "${outdir:-}" || -z "${prefix:-}" ]]; then
    echo "Error: --input, --outdir, and --prefix are required"
    exit 1
fi
if [[ ! -d "$TMPDIR" ]]; then
    echo "Error: TMPDIR '$TMPDIR' does not exist"
    exit 1
fi
which bcftools >/dev/null 2>&1 || { echo "bcftools not found in PATH"; exit 1; }

mkdir -p "$outdir"

echo "# getting contigs from VCF: $input_vcf"
mapfile -t contigs < <(grep "^##contig" "${input_vcf}" | \
  cut -d ',' -f 1 | cut -d '=' -f 3 )

if [[ "${vcf_needs_bgz:-false}" == true ]]; then
    echo "# preparing input VCF by bgzipping and indexing"
    mktemp_vcf_bgz=$(mktemp "$TMPDIR/tmp_vcf_bgz.XXXXXX") || { echo "failed to create temporary bgzipped VCF file"; exit 1; }
    trap 'rm -f "$mktemp_vcf_bgz" "${mktemp_vcf_bgz}.tbi"' EXIT
    bgzip -c "$input_vcf" > "$mktemp_vcf_bgz"
    tabix -p vcf "$mktemp_vcf_bgz"
    input_vcf="$mktemp_vcf_bgz"
fi
echo "# splitting VCF by contig into directory: $outdir"
for contig in "${contigs[@]}"; do
    echo "# processing contig: $contig"
    output_vcf="${outdir}/${prefix}.${contig}.vcf"
    bcftools view -r "$contig" -O v -o "${output_vcf}" "$input_vcf"
    echo "# wrote contig VCF: $output_vcf"
done
echo "# done"
echo "# elapsed time: $(( $(date +%s) - t_0 )) seconds"






