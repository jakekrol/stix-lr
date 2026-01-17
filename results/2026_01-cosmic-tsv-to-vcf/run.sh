#!/usr/bin/env bash
tmp='/data/jake/tmp'

tsv_cosmic='../../data/2025_11-cosmic_sv/Cosmic_StructuralVariants_v103_GRCh38.tsv.gz'
vcf_cosmic='cosmic.v103.grch38.vcf'
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

echo "# converting cosmic tsv to bed"
./cosmic_tsv2bed.py





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
##INFO=<ID=END,Number=1,Type=Integer,Description="End position of structural variation">
##INFO=<ID=CHR2,Number=1,Type=String,Description="Mate chromsome for BND SVs">
##INFO=<ID=COSMIC_STRUCTURAL_ID,Number=1,Type=String,Description="COSMIC structural variant ID">
##INFO=<ID=COSMIC_SAMPLE_ID,Number=1,Type=String,Description="COSMIC sample ID">
##INFO=<ID=COSMIC_SAMPLE_NAME,Number=1,Type=String,Description="COSMIC sample name">
##INFO=<ID=AC,Number=A,Type=Integer,Description="Alternate allele count in genotypes">
##INFO=<ID=AN,Number=A,Type=Integer,Description="Total number of alleles in called genotypes">
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele frequency">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
EOF
printf "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tCOSMIC\n" >> $vcf_cosmic

# add the variants from cosmic.bed here
# cosmic.bed format (tab-separated):
#   CHROM  START  END  SVTYPE  SVLEN  COSMIC_STRUCTURAL_ID  COSMIC_SAMPLE_ID  SAMPLE_NAME
awk 'BEGIN { FS = OFS = "\t" }
    NR == 1 { next }  # skip header
    {
        chrom = $1
        start = $2
        end   = $3
        svtype = $4
        svlen  = $5
        cosmic_struct_id = $6
        cosmic_sample_id = $7
        sample_name = $8

        # For deletions, SVLEN must be negative per VCF spec
        if (svtype == "DEL" && svlen > 0) {
            svlen = -svlen
        }

           # Minimal VCF record with INFO fields SVTYPE, SVLEN, END and
           # dummy frequency/genotype info so Truvari/needLR can compute AF.
           # Treat each variant as homozygous-alt in a single diploid sample:
           #   AC=2, AN=2, AF=1.0, GT=1/1
           info = sprintf("SVTYPE=%s;SVLEN=%s;END=%s;AC=2;AN=2;AF=1.0;COSMIC_STRUCTURAL_ID=%s;COSMIC_SAMPLE_ID=%s;COSMIC_SAMPLE_NAME=%s",
                       svtype, svlen, end, cosmic_struct_id, cosmic_sample_id, sample_name)
           printf "%s\t%s\t%s\tN\t<%s>\t.\tPASS\t%s\tGT\t1/1\n",
               chrom, start, cosmic_struct_id, svtype, info
    }' cosmic.bed >> "$vcf_cosmic"
echo "# cosmic vcf created at $vcf_cosmic"