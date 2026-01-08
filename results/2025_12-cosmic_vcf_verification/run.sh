#!/usr/bin/env bash
tmp='/data/jake/tmp'

mutation_type2acronym() {
    local mutation_type="$1"
    mutation_type=$(echo "$mutation_type" | tr '[:upper:]' '[:lower:]')
    case "$mutation_type" in
        "interchromosomal insertion") echo "INS" ;;
        "interchromosomal reciprocal translocation") echo "BND" ;;
        "intrachromosomal deletion" ) echo "DEL" ;;
        "intrachromosomal fold-back inversion") echo "INV" ;;
        "intrachromosomal inversion") echo "INV" ;;
        "intrachromosomal tandem duplication") echo "DUP" ;;
        *) echo "UNK" ;;  # Unknown type
    esac
}

bed_svafatote='../../data/2025_11-svafotate_bed/SVAFotate_core_SV_popAFs.GRCh38.v4.1.bed.gz'
tsv_cosmic='../../data/2025_11-cosmic_sv/Cosmic_StructuralVariants_v103_GRCh38.tsv.gz'
vcf_cosmic='cosmic.v103.grch38.vcf'
# svafotate bed
echo "# decompressing svafotate bed"
if [ -f svafotate.bed ]; then
    echo "# svafotate.bed already exists, skipping decompression"
else
    bgzip -dc $bed_svafatote > svafotate.bed
fi
# cosmic tsv
echo "# decompressing cosmic tsv"
if [ -f cosmic.tsv ]; then
    echo "# cosmic.tsv already exists, skipping decompression"
else
    gunzip -c $tsv_cosmic > cosmic.tsv
fi
echo "# removing abnormal mutation types"
grep -v -i "unknown type" cosmic.tsv | \
grep -v -i "with inverted orientation" | \
grep -v -i "with non-inverted orientation" | \
grep -v -i "amplicon" | \
grep -v -i "multi-component rearrangement" > \
    cosmic.filtered.tsv




# make a cosmic vcf
echo "# making cosmic vcf header"
cat > $vcf_cosmic << 'EOF'
##fileformat=VCFv4.2
##contig=<ID=chr1,length=248956422>
##contig=<ID=chr2,length=242193529>
##contig=<ID=chr3,length=198295559>
##contig=<ID=chr4,length=190214555>
##contig=<ID=chr5,length=181538259>
##contig=<ID=chr6,length=170805979>
##contig=<ID=chr7,length=159345973>
##contig=<ID=chr8,length=145138636>
##contig=<ID=chr9,length=138394717>
##contig=<ID=chr10,length=133797422>
##contig=<ID=chr11,length=135086622>
##contig=<ID=chr12,length=133275309>
##contig=<ID=chr13,length=114364328>
##contig=<ID=chr14,length=107043718>
##contig=<ID=chr15,length=101991189>
##contig=<ID=chr16,length=90338345>
##contig=<ID=chr17,length=83257441>
##contig=<ID=chr18,length=80373285>
##contig=<ID=chr19,length=58617616>
##contig=<ID=chr20,length=64444167>
##contig=<ID=chr21,length=46709983>
##contig=<ID=chr22,length=50818468>
##contig=<ID=chr23,length=156040895>
##contig=<ID=chr24,length=57227415>
##contig=<ID=chrM,length=16569>
##contig=<ID=chrX,length=156040895>
##contig=<ID=chrY,length=57227415>
##ALT=<ID=INS,Description="Insertion">
##ALT=<ID=DEL,Description="Deletion">
##ALT=<ID=DUP,Description="Duplication">
##ALT=<ID=INV,Description="Inversion">
##ALT=<ID=BND,Description="Breakend; Translocation">
##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variation">
##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Length of structural variation">
##INFO=<ID=END,Number=1,Type=String,Description="End position of structural variation">
##INFO=<ID=CHR2,Number=1,Type=String,Description="Mate chromsome for BND SVs">
EOF
printf "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n" >> $vcf_cosmic

n=$(wc -l < cosmic.filtered.tsv)
i=1
echo "# processing cosmic.filtered.tsv with $n entries"
# while IFS=$'\t' read -r -a fields; do
#     # skip header
#     [[ "${fields[0]}" == "SAMPLE_NAME" ]] && continue
#     sample_name="${fields[0]}"
#     cosmic_sample_id="${fields[1]}"
#     cosmic_phenotype_id="${fields[2]}"
#     cosmic_structural_id="${fields[3]}"
#     mutation_type="${fields[4]}"
#     chromosome_from="${fields[8]}"
#     chromosome_to="${fields[9]}"
#     location_from_min="${fields[10]}"
#     location_from_max="${fields[11]}"
#     location_to_min="${fields[12]}"
#     location_to_max="${fields[13]}"
#     strand_from="${fields[14]}"
#     strand_to="${fields[15]}"

#     # parse
#     mutation_type_acronym=$(mutation_type2acronym "$mutation_type")
#     svlen=$((location_to_max - location_from_min))

#     # debug
#     # Add debug output before the svlen calculation
#     echo "DEBUG: $cosmic_structural_id - $mutation_type" >&2
#     echo "  from_min=$location_from_min, from_max=$location_from_max" >&2
#     echo "  to_min=$location_to_min, to_max=$location_to_max" >&2
#     echo "  strand_from=$strand_from, strand_to=$strand_to" >&2
#     echo "  calculated svlen=$svlen" >&2
#     echo "---" >&2

#     # build VCF line
#     line="chr${chromosome_from}\t"
#     line+="${location_from_min}\t"
#     line+="COSMIC_SV_${cosmic_structural_id}\t"
#     line+="N\t"
#     line+="<${mutation_type_acronym}>\t"
#     line+=".\t"
#     line+="PASS\t"
#     line+="SVTYPE=${mutation_type_acronym};"
#     line+="SVLEN=${svlen};"
#     line+="END=${location_to_max};"
#     line+="CHR2=${chromosome_to};"

#     echo -e "$line" >> $vcf_cosmic
#     if (( i % 1000 == 0 )); then
#         echo "# processed $i of $n entries"
#     fi
#     ((i++))
# done < cosmic.filtered.tsv
while IFS=$'\t' read -r -a fields; do
    # skip header
    [[ "${fields[0]}" == "SAMPLE_NAME" ]] && continue
    
    sample_name="${fields[0]}"
    cosmic_sample_id="${fields[1]}"
    cosmic_phenotype_id="${fields[2]}"
    cosmic_structural_id="${fields[3]}"
    mutation_type="${fields[4]}"
    description="${fields[5]}"
    pubmed_pmid="${fields[6]}"
    cosmic_study_id="${fields[7]}"
    chromosome_from="${fields[8]}"
    chromosome_to="${fields[9]}"
    location_from_min="${fields[10]}"
    location_from_max="${fields[11]}"
    location_to_min="${fields[12]}"
    location_to_max="${fields[13]}"
    strand_from="${fields[14]}"
    strand_to="${fields[15]}"


    # parse
    mutation_type_acronym=$(mutation_type2acronym "$mutation_type")
    

    # Calculate coordinates based on SV type
    if [[ "$mutation_type_acronym" == "DEL" ]]; then
        # Use proper coordinate order for deletions
        start_pos=$(( location_from_min < location_to_min ? location_from_min : location_to_min ))
        end_pos=$(( location_from_max > location_to_max ? location_from_max : location_to_max ))
        vcf_pos="$start_pos"
        vcf_end="$end_pos"
        svlen=$(( start_pos - end_pos ))  # Negative
    elif [[ "$mutation_type_acronym" == "INS" ]]; then
        vcf_pos="$location_from_min"
        vcf_end="$location_from_min"      # Same position for insertions
        svlen=$(( location_to_max - location_from_min ))  # Positive
    else
        vcf_pos="$location_from_min"
        vcf_end="$location_to_max"
        svlen=$(( location_to_max - location_from_min ))
    fi


    # build VCF line using calculated coordinates
    line="chr${chromosome_from}\t"
    line+="${vcf_pos}\t"                  # Use calculated vcf_pos
    line+="COSMIC_SV_${cosmic_structural_id}\t"
    line+="N\t"
    line+="<${mutation_type_acronym}>\t"
    line+=".\t"
    line+="PASS\t"
    line+="SVTYPE=${mutation_type_acronym};"
    line+="SVLEN=${svlen};"
    line+="END=${vcf_end};"               # Use calculated vcf_end
    line+="CHR2=chr${chromosome_to};"

    echo -e "$line" >> $vcf_cosmic
    if (( i % 1000 == 0 )); then
        echo "# processed $i of $n entries"
    fi
    ((i++))
done < cosmic.filtered.tsv
echo "# finished making cosmic vcf: $vcf_cosmic"

# split cosmic vcf by contig
split_by_contig.sh \
    --input "$vcf_cosmic" \
    --outdir "$(pwd)" \
    --tempdir "$tmp" \
    --prefix "cosmic.v103.grch38" \
    --vcf_needs_bgz

# rm any empty contig vcfs
for f in cosmic.v103.grch38.chr*.vcf; do
    if [[ ! -s "$f" ]]; then
        echo "# removing empty vcf: $f"
        rm -f "$f"
    fi
done

