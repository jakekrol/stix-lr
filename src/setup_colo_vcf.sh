#!/usr/bin/env bash
set -euo pipefail

SED_FILE='/data/jake/stix-lr/src/setup_vcf.sed'
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -i|--input)
            INPUT_FILE="$2"
            shift
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift
            ;;
        --sedfile)
            SED_FILE="$2"
            shift
            ;;
        -h|--help)
            echo "Usage: setup_colo_vcf.sh [options]"
            echo ""
            echo "Options:"
            echo "  -h, --help        Show this help message and exit"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information."
            exit 1
            ;;
    esac
    shift
done

main () {
    echo "Input file: $INPUT_FILE"
    echo "Output file: $OUTPUT_FILE"
    echo "Filtering BNDs"
    bcftools view --exclude 'INFO/SVTYPE="BND"' "$INPUT_FILE" > "$OUTPUT_FILE".tmp1.vcf
    echo "Setting END type and AF header line"
    sed -f "$SED_FILE" "$OUTPUT_FILE".tmp1.vcf > "$OUTPUT_FILE"
    rm "$OUTPUT_FILE".tmp1.vcf
    echo "Done. Output written to $OUTPUT_FILE"
}
main