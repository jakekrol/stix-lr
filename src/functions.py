import os

def extract_maxaf(vcf_annotated, outfile):
    '''
    extract Max_AF from svafotate annotated VCF using bcftools
    '''
    # Use direct path to bcftools executable
    cmd = f"bcftools query -f '%INFO/Max_AF\n' {vcf_annotated} > {outfile}"
    print("Running cmd:", cmd)
    result = os.system(cmd)
    if result != 0:
        print(f"Error extracting Max_AF for {vcf_annotated}: exit code {result}")

def read_maxaf_file(filepath):
    """Read max AF values from a file and return as a list of floats"""
    maxaf_values = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    maxaf_values.append(float(line))
                except ValueError:
                    print(f"Warning: Could not convert line to float: {line}")
    return maxaf_values