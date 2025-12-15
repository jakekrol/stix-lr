#!/usr/bin/env python3
import argparse
import os,sys
import pandas as pd
import time
import matplotlib.pyplot as plt
from functions import extract_maxaf, read_maxaf_file

t_0 = time.time()
parser = argparse.ArgumentParser(description="Plot stix lr cosmic sv pop freq")
parser.add_argument("--input_stix_lr", required=True, help="Input stix lr cosmic pop freq tsv file")
parser.add_argument("--input_svafotate", required=True, help="Input svafotate cosmic pop freq tsv file")
parser.add_argument("--output_dir", required=True, help="Output directory")

def validation(args):
    assert os.path.exists(args.input_stix_lr), f"Input file does not exist: {args.input_stix_lr}"
    assert os.path.exists(args.input_svafotate), f"Input file does not exist: {args.input_svafotate}"


def main():
    # args
    args = parser.parse_args()
    validation(args)
    # input
    df = pd.read_csv(args.input_stix_lr, sep="\t")
    svafotate_popfreq_file = os.path.join(args.output_dir, "svafotate_pop_freq.txt")
    extract_maxaf(
        args.input_svafotate,
        svafotate_popfreq_file
    )
    svafotate_popfreq = read_maxaf_file(svafotate_popfreq_file)
    # get csum data
    svafotate_popfreq = pd.Series(svafotate_popfreq, name='pop_freq')
    svafotate_popfreq_counts = svafotate_popfreq.value_counts().sort_index()

    svafotate_popfreq_counts_csum = svafotate_popfreq_counts.cumsum()
    svafotate_x = [-0.00001] + svafotate_popfreq_counts_csum.index.tolist() + [1.0]
    svafotate_y = [0] + svafotate_popfreq_counts_csum.tolist() + [max(svafotate_popfreq_counts_csum.tolist())]

    df_stix = df.sort_values(by='pop_freq', ascending=True).reset_index(drop=True)
    stix_popfreq_counts = df.groupby('pop_freq').size()
    stix_popfreq_counts_csum = stix_popfreq_counts.cumsum()
    stix_x = [-0.00001] + stix_popfreq_counts_csum.index.tolist()
    stix_y = [0] + stix_popfreq_counts_csum.tolist()
    # plot
    plt.figure()
    plt.plot(stix_x, stix_y, label='stix lr')
    plt.plot(svafotate_x, svafotate_y, label='svafotate')
    plt.xlabel('Population Frequency')
    plt.ylabel('Count')
    plt.title('Cumulative COSMIC \nSV Count vs Population Frequency')
    plt.legend()
    plt.savefig(args.output_dir + '/cosmic_popfreq_cumsum_plot.png')
    print(f"# plot saved to {args.output_dir + '/cosmic_popfreq_cumsum_plot.png'}")
    print(f"# elapsed time: {time.time()-t_0:.3f} seconds")

if __name__ == "__main__":
    main()
