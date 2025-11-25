#!/usr/bin/env python3

import argparse
import os
import sys
import shutil
import itertools
import time

# args
def get_args():
    parser = argparse.ArgumentParser(description="Run SVAFotate for somatic variant annotation in colo")
    parser.add_argument("--input", required=True, help="Input VCF file")
    parser.add_argument("--bed", required=True, help="SVAFotate BED file")
    parser.add_argument("--outdir", required=True, help="Output directory")
    parser.add_argument("--scriptdir", required=True, help="Directory containing necessary scripts")
    parser.add_argument("-p", "--cpus", type=int, default=1, help="Number of CPUs to use")
    parser.add_argument("--env_name", default="svafotate-env", help="Conda environment name for SVAFotate")
    args = parser.parse_args()
    return args

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

# def conda_activate_cmd(env_name):
#     return f"eval $(conda shell.bash hook) && conda activate {env_name}"


def validate_args(args):
    # validate I/O
    assert os.path.isfile(args.input), f"Input file {args.input} does not exist"
    assert os.path.isfile(args.bed), f"BED file {args.bed} does not exist"
    os.makedirs(args.outdir, exist_ok=True) 

    # scripts
    scripts = ["setup_colo_vcf.sh", "setup_vcf.sed", "svafotate_install.sh"]
    for script in scripts:
        script_path = os.path.join(args.scriptdir, script)
        assert os.path.isfile(script_path), f"Required script {script} not found in {args.scriptdir}"

def setup_in_vcf(input_vcf, outdir, scriptdir):
    setup_script = os.path.join(scriptdir, "setup_colo_vcf.sh")
    sed_script = os.path.join(scriptdir, "setup_vcf.sed")
    cln_vcf = os.path.join(outdir, os.path.basename(input_vcf).replace('.vcf', '_cln.vcf'))
    cmd = f"{setup_script} -i {input_vcf} -o {cln_vcf} --sedfile {sed_script}"
    print("Running cmd:", cmd)
    os.system(cmd)
    return cln_vcf

def run_svafotate(cln_vcf, bed_file, outdir, outfile, scriptdir, cpus, env_name, overlap, source):
    # Use direct path to svafotate executable instead of conda activate
    svafotate_exe = get_conda_exe_path(env_name, 'svafotate')
    cmd = f"{svafotate_exe} annotate -v {cln_vcf} -b {bed_file} " \
        f"-f {overlap} -s {source} -O vcf -o {outfile} --cpu {cpus}"
    print("Running cmd:", cmd)
    result = os.system(cmd)
    if result != 0:
        print(f"Error running svafotate for {cln_vcf}: exit code {result}")
    return outfile

def get_overlap_params():
    return {0.5,0.6,0.7,0.8,0.9}

def get_sources():
    return {"CCDG", "gnomAD", "ThousG", "TOPMed"}

def extract_maxaf(vcf_annotated, outfile, env_name):
    # Use direct path to bcftools executable
    bcftools_exe = get_conda_exe_path(env_name, 'bcftools')
    cmd = f"{bcftools_exe} query -f '%INFO/Max_AF\n' {vcf_annotated} > {outfile}"
    print("Running cmd:", cmd)
    result = os.system(cmd)
    if result != 0:
        print(f"Error extracting Max_AF for {vcf_annotated}: exit code {result}")

def main():
    t_begin = time.time()
    args = get_args()
    validate_args(args)

    # Setup input VCF
    cln_vcf = setup_in_vcf(args.input, args.outdir, args.scriptdir)

    # Run SVAFotate for each combination of overlap fractions and sources
    overlap_params = get_overlap_params()
    sources = get_sources()
    combos = itertools.product(overlap_params, sources)
    print("Starting SVAFotate experiments...")
    for overlap, source in combos:
        t_0 = time.time()
        out_vcf = os.path.join(args.outdir, f"svafotate-overlap_{(overlap)}-source_{source}.vcf")
        print(f"Running SVAFotate for overlap {overlap}, source {source}")
        svafotate_vcf = run_svafotate(
            cln_vcf,
            args.bed,
            args.outdir,
            out_vcf,
            args.scriptdir,
            args.cpus,
            args.env_name,
            overlap,
            source
        )
        # do max af extraction here
        print(f"Extracting Max_AF for overlap {overlap}, source {source}")
        extract_maxaf(svafotate_vcf, out_vcf.replace('.vcf', '_maxaf.txt'), args.env_name)
        print(f"SVAFotate completed for overlap {overlap}, source {source} in {time.time() - t_0:.2f} seconds")
    print("All SVAFotate experiments completed.")
    print(f"Total time elapsed: {time.time() - t_begin:.2f} seconds")

        
if __name__ == "__main__":
    main()
    


