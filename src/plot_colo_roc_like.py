#!/usr/bin/env python3

import matplotlib.pyplot as plt
import argparse
import os,sys
import re
import numpy as np
import pandas as pd
from tqdm import tqdm
import time

parser = argparse.ArgumentParser(description="Plot SVAFotate annotation results for colo")
parser.add_argument("--dirgermline", required=True, help="Dir with SVAFotate annotated germline results")
parser.add_argument("--dirsomatic", required=True, help="Dir with SVAFotate annotated somatic results")
parser.add_argument("--output_dir", required=True, help="Output dir")
parser.add_argument("--file_pattern", help="File name pattern to filter input files")
parser.add_argument("--cache", action='store_true', help="Use cached results if available")
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
            params['overlap'] = float(overlap)
        elif p.startswith('source'):
            source = p.split('_')[1]
            params['source'] = source
    return params

def pair_germline_somatic_files(dirgermline, dirsomatic):
    ''' pair by overlap and source params '''
    germline_files = [f for f in os.listdir(dirgermline) if f.endswith('.txt')]
    somatic_files = [f for f in os.listdir(dirsomatic) if f.endswith('.txt')]
    paired_files = []
    for gf in germline_files:
        gparams = fname2params(gf)
        for sf in somatic_files:
            if args.file_pattern:
                if not re.search(args.file_pattern, gf) or not re.search(args.file_pattern, sf):
                    continue
            sparams = fname2params(sf)
            # dictionary equality check
            if gparams == sparams:
                paired_files.append(
                    # (os.path.join(dirgermline, gf), os.path.join(dirsomatic, sf), gparams)
                    (os.path.join(dirgermline, gf), os.path.join(dirsomatic, sf), gparams['overlap'])
                )
    return paired_files

def file_pair2score_tbl(f_germline,f_somatic):
    pop_freq_germline = read_maxaf_file(f_germline)
    df_germline = pd.DataFrame(
        {'pop_freq': pop_freq_germline,
         'source': ['germline']*len(pop_freq_germline)
        }
    )
    df_somatic = pd.DataFrame(
        {'pop_freq': read_maxaf_file(f_somatic),
         'source': ['somatic']*len(read_maxaf_file(f_somatic))
        }
    )
    df_comb = pd.concat([df_germline, df_somatic], ignore_index=True)
    df_comb = df_comb.sort_values(by='pop_freq', ascending=True)
    return df_comb


def score2roc(df_score):
    # get unique thresholds to sweep
    thresholds = sorted(df_score['pop_freq'].unique())
    # min: all assigned germline for visualization purposes
    min_thresh = df_score['pop_freq'].min() - 1e-6
    thresholds = [min_thresh] + thresholds
    tpr_list = []
    fpr_list = []
    # positives are all somatics
    P = sum(df_score['source'] == 'somatic')
    # negatives are all germlines
    N = sum(df_score['source'] == 'germline')
    # this is really slow and inefficient
    for thresh in tqdm(thresholds, desc="Computing ROC points"):
        # tps are somatics beloweq threshold
        TP = sum((df_score['pop_freq'] <= thresh) & (df_score['source'] == 'somatic'))
        # fps are germlines beloweq threshold
        FP = sum((df_score['pop_freq'] <= thresh) & (df_score['source'] == 'germline'))
        P_hat = TP + FP
        TPR = TP / P
        FPR = FP / N
        tpr_list.append(TPR)
        fpr_list.append(FPR)
    df = pd.DataFrame({'threshold': thresholds, 'tpr': tpr_list, 'fpr': fpr_list})
    return df

def main():
    t_0 = time.time()
    print("# validating input")
    validation(args)
    print("# pairing germline and somatic files")
    # load pop freqs for svs
    paired_files = pair_germline_somatic_files(args.dirgermline, args.dirsomatic)
    # compute roc points
    if args.cache:
        cache_file = os.path.join(args.output_dir, "colo_svafotate_roc_data.tsv")
        if os.path.exists(cache_file):
            print(f"# loading cached ROC data from {cache_file}")
            df_roc_all = pd.read_csv(cache_file, sep="\t")
    else:
        df_roc_all = pd.DataFrame()
        for germline,somatic,overlap in paired_files:
            print(f"# processing pair: {germline}, {somatic} (overlap={overlap})")
            df_score = file_pair2score_tbl(germline,somatic)
            df_roc = score2roc(df_score)
            df_roc['overlap'] = overlap
            # plt.plot(fpr, tpr, marker='o', label=f'overlap={overlap}')
            df_roc_all = pd.concat([df_roc_all, df_roc], ignore_index=True)
        df_roc_all.to_csv(
            os.path.join(args.output_dir, "colo_svafotate_roc_data.tsv"),
            sep="\t",
            index=False
        )
        print(f"# wrote ROC data to {os.path.join(args.output_dir, 'colo_svafotate_roc_data.tsv')}")
    # plot
    plt.figure()
    for overlap, df_subset in df_roc_all.groupby('overlap'):
        plt.plot(df_subset['fpr'], df_subset['tpr'], label=f'overlap={overlap}')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('SVAFotate COLO somatic classification\n by pop. freq. threshold')
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
    plt.legend(title='Overlap fraction', loc='lower right')
    plt.tight_layout()
    outplot = os.path.join(args.output_dir, "colo_svafotate_roc_curve.png")
    print(f"# plotting ROC to {outplot}")
    plt.savefig(outplot)
    print(f"# total time elapsed: {time.time() - t_0:.2f} seconds")

if __name__ == "__main__":
    main()
