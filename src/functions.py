import os
import subprocess

def get_conda_exe_path(env_name, executable):
    """Get full path to executable in conda environment"""
    # Get conda base path from CONDA_EXE environment variable
    conda_exe = os.environ.get('CONDA_EXE')
    if conda_exe:
        conda_base = os.path.dirname(os.path.dirname(conda_exe))  # Remove /bin/conda
    else:
        # Fallback to common conda locations
        conda_base = os.path.expanduser('~/miniconda3')
        if not os.path.exists(conda_base):
            conda_base = os.path.expanduser('~/anaconda3')
    
    # Try multiple locations for the executable
    search_paths = [
        # 1. Environment-specific bin directory
        os.path.join(conda_base, 'envs', env_name, 'bin', executable),
        # 2. Base conda bin directory
        os.path.join(conda_base, 'bin', executable),
        # 3. Use which command to find in PATH (current environment)
        None  # Placeholder for which command
    ]
    
    # Check environment and base conda paths
    for path in search_paths[:2]:
        if os.path.exists(path):
            return path
    
    # If not found, try using 'which' command to find in current PATH
    import subprocess
    try:
        result = subprocess.run(['which', executable], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    # If still not found, just return the executable name (let PATH handle it)
    print(f"Warning: Could not find full path for '{executable}', using executable name directly")
    return executable

def extract_stix_one(vcf_annotated, outfile, mode = 'w'):
    '''
    extract STIX_ONE from stix lr annotated VCF using bcftools
    '''
    if mode == 'w':
        cmd = f"bcftools query -f '%ID\t%INFO/STIX_ONE\n' {vcf_annotated} > {outfile}"
    elif mode == 'a':
        cmd = f"bcftools query -f '%ID\t%INFO/STIX_ONE\n' {vcf_annotated} >> {outfile}"
    else:
        raise ValueError("mode must be 'w' or 'a'")
    print("Running cmd:", cmd)
    result = os.system(cmd)
    if result != 0:
        print(f"Error extracting STIX_ONE for {vcf_annotated}: exit code {result}")

def extract_maxaf(vcf_annotated, outfile, mode = 'w'):
    '''
    extract Max_AF from svafotate annotated VCF using bcftools
    '''
    # Use direct path to bcftools executable
    if mode == 'w':
        cmd = f"bcftools query -f '%ID\t%INFO/Max_AF\n' {vcf_annotated} > {outfile}"
    elif mode == 'a':
        cmd = f"bcftools query -f '%ID\t%INFO/Max_AF\n' {vcf_annotated} >> {outfile}"
    else:
        raise ValueError("mode must be 'w' or 'a'")
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
