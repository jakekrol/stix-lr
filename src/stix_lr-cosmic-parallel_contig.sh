#!/usr/bin/env bash
set -euo pipefail
t_0=$(date +%s)

SHARDFILE="shardfile.txt"
INDEX="/data/jake/stix-lr-grch38"
MIN_READS=(1 5)
while [[ $# -gt 0 ]]; do
    case $1 in
        --indir)
            indir="$2"
            shift 2
            ;;
        --outdir)
            outdir="$2"
            shift 2
            ;;
        --tempdir)
            temp_dir="$2"
            export TMPDIR="$temp_dir"
            shift 2
            ;;
        --index)
            INDEX="$2"
            shift 2
            ;;
        --shardfile)
            SHARDFILE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done
# validation
if [[ -z "${indir:-}" || -z "${outdir:-}" ]]; then
    echo "Error: --indir and --outdir are required"
    exit 1
fi
if [[ ! -d "$INDEX" ]]; then
    echo "Error: INDEX directory '$INDEX' does not exist"
    exit 1
fi
# default tmp
TMPDIR="${TMPDIR:-/tmp}"
if [[ ! -d "$TMPDIR" ]]; then
    echo "Error: TMPDIR '$TMPDIR' does not exist"
    exit 1
fi
# preserve paths
outdir="$(realpath "$outdir")"
indir="$(realpath "$indir")"
# need to run stix from INDEX dir
cd "$INDEX" || { echo "Error: Could not change to directory $INDEX"; exit 1; }
if [[ ! -f "$SHARDFILE" ]]; then
    echo "Error: Shardfile '$SHARDFILE' does not exist"
    exit 1
fi

mkdir -p "$outdir"
echo "# getting vcfs from indir: $indir"
mapfile -t vcf_files < <(ls "${indir}"/*.vcf)
echo "# processing ${#vcf_files[@]} vcfs"
echo "# setting up temp files"
input=$(mktemp "$TMPDIR/input_XXXXXX.txt")
trap 'rm -f "$input"' EXIT
procs=${#vcf_files[@]}
for min_reads in "${MIN_READS[@]}"; do
    for vcf in "${vcf_files[@]}"; do
        base=$(basename "$vcf" .vcf)
        printf "%s\t%s\t%s\t%s\n" "$vcf" "$min_reads" "$SHARDFILE" \
            "${outdir}/${base}.stix_lr.min_read_${min_reads}.vcf" >> "$input"
    done
done
echo "# using $input as temp input file to gargs"
echo "# running stix lr in parallel with $procs processes"
cat "$input" | gargs --log "${outdir}/stix_lr-colo-parallel_contig.log" \
    -p "$procs" \
    'stix -f {0} -T {1} -s 500 -B {2} > {3}'

t_elapsed=$(( $(date +%s) - t_0 ))
echo "# all done. elapsed time: ${t_elapsed} seconds."