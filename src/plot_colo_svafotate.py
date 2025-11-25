#!/usr/bin/env python3

import matplotlib.pyplot as plt
import argparse
import os,sys
import re
import numpy as np

parser = argparse.ArgumentParser(description="Plot SVAFotate annotation results for colo")
parser.add_argument("--dirgermline", required=True, help="Dir with SVAFotate annotated germline results")
parser.add_argument("--dirsomatic", required=True, help="Dir with SVAFotate annotated somatic results")
parser.add_argument("--output", required=True, help="Output plot file path")
args = parser.parse_args()

def validation(args):
    assert os.path.exists(args.dirgermline), f"Germline directory does not exist: {args.dirgermline}"
    assert os.path.exists(args.dirsomatic), f"Somatic directory does not exist: {args.dirsomatic}"

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

def fname2params(filename):
    """Extract parameters from filename"""
    base = os.path.basename(filename)
    params = {}
    parts = base.split('-')
    parts.remove('svafotate')
    parts[-1] = parts[-1].replace('.txt', '')
    for p in parts:
        if p.startswith('overlap'):
            overlap = p.split('_')[1]
            params['overlap'] = overlap
        elif p.startswith('source'):
            source = p.split('_')[1]
            params['source'] = source
    return params

def bar_subplot(ax, x_germline, x_somatic, overlap, source):
    # horizontal axis are bins of max AF values {0, (0,1%], (1%,5%], (5%,100%]}
    # vertical axis is log10 count of variants in each bin
    
    # Handle exact zeros separately
    germline_zeros = np.sum(np.array(x_germline) == 0)
    somatic_zeros = np.sum(np.array(x_somatic) == 0)
    
    # Filter out zeros for histogram of non-zero values
    germline_nonzero = [x for x in x_germline if x > 0]
    somatic_nonzero = [x for x in x_somatic if x > 0]
    
    # Bins for non-zero values: (0, 1%], (1%, 5%], (5%, 100%]
    nonzero_bins = [1e-10, 0.01, 0.05, 1.0]  # Start just above 0
    labels = ['0%', '(0-1%]', '(1%-5%]', '(5%-100%]']
    
    # Get counts for non-zero bins
    germline_nonzero_counts, _ = np.histogram(germline_nonzero, bins=nonzero_bins)
    somatic_nonzero_counts, _ = np.histogram(somatic_nonzero, bins=nonzero_bins)
    
    # Combine zero counts with non-zero counts
    germline_counts = np.array([germline_zeros] + list(germline_nonzero_counts))
    somatic_counts = np.array([somatic_zeros] + list(somatic_nonzero_counts))
    
    x = np.arange(len(labels)) # the label locations
    width = 0.35  # the width of the bars
    ax.bar(x - width/2, np.log10(germline_counts + 1), alpha=1, label='Germline', color='lightblue', width=width)
    ax.bar(x + width/2, np.log10(somatic_counts + 1), alpha=1, label='Somatic', color='magenta', width=width)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Log10(Count + 1)')
    ax.set_title(f'Overlap: {overlap}, Source: {source}')
    # Add a legend
    ax.legend()
    return ax

def pair_germline_somatic_files(dirgermline, dirsomatic):
    ''' pair by overlap and source params '''
    germline_files = [f for f in os.listdir(dirgermline) if f.endswith('.txt')]
    somatic_files = [f for f in os.listdir(dirsomatic) if f.endswith('.txt')]
    paired_files = []
    for gf in germline_files:
        gparams = fname2params(gf)
        for sf in somatic_files:
            sparams = fname2params(sf)
            # dictionary equality check
            if gparams == sparams:
                paired_files.append(
                    (os.path.join(dirgermline, gf), os.path.join(dirsomatic, sf), gparams)
                )
    return paired_files

def plot_af_comparison(args, paired_files):
    fig, axes = plt.subplots(5, 4, figsize=(20, 25))
    
    # Define order: rows = overlap (0.5 to 0.9), columns = sources
    overlap_order = ['0.5', '0.6', '0.7', '0.8', '0.9']
    source_order = ['CCDG', 'gnomAD', 'ThousG', 'TOPMed']
    
    # Create mapping from (overlap, source) to subplot position
    overlap_to_row = {overlap: i for i, overlap in enumerate(overlap_order)}
    source_to_col = {source: j for j, source in enumerate(source_order)}
    
    # Process each file pair
    for germline_file, somatic_file, params in paired_files:
        x_germline = read_maxaf_file(germline_file)
        x_somatic = read_maxaf_file(somatic_file)
        overlap = params['overlap']
        source = params['source']
        axes[overlap_to_row[overlap], source_to_col[source]] = bar_subplot(
            axes[overlap_to_row[overlap], source_to_col[source]], 
            x_germline, 
            x_somatic, 
            overlap, 
            source
        )
    # Add row and column labels
    for i, overlap in enumerate(overlap_order):
        axes[i, 0].set_ylabel(f'Overlap {overlap}\nLog10(Count + 1)', fontweight='bold')
    
    for j, source in enumerate(source_order):
        axes[0, j].set_title(f'{source}\n{axes[0, j].get_title()}', fontweight='bold')
    
    # Add overall title
    # fig.suptitle('SVAFotate Analysis: Germline vs Somatic Max AF Distribution\nRows: Overlap Threshold, Columns: Source Dataset', 
    #              fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    plt.savefig(args.output)
    print(f"Plot saved to {args.output}")
    plt.close()

def main():
    print("Validating input arguments...")
    validation(args)
    print("Pairing germline and somatic files...")
    paired_files = pair_germline_somatic_files(args.dirgermline, args.dirsomatic)
    print("Generating plot...")
    plot_af_comparison(args, paired_files)
    print("Done.")

if __name__ == "__main__":
    main()

