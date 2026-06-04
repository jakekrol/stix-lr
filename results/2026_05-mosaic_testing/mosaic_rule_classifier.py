#!/usr/bin/env python

import argparse
import sys
import numpy as np


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i',
                        type=str,
                        default='../../data/2026_04-mosaic_ryan/te_mosiac_agg.allele_ballance.lessmd.rm_missing.tsv')
    parser.add_argument('--sample-col',
                        type=int,
                        default=4,
                        help='First column index of per-sample values (default 4)')
    parser.add_argument('--mosaic_region_density_lower_bound',
                        type=float,
                        default=0.2)
    parser.add_argument('--mosaic_region_saf_lower_bound',
                        type=float,
                        default=0.2)
    parser.add_argument('--mosaic_region_saf_upper_bound',
                        type=float,
                        default=0.4)
    parser.add_argument('--high_saf_density_upper_bound',
                        type=float,
                        default=1.0)
    parser.add_argument('--output', '-o',
                        type=str,
                        default='mosaic_classification.tsv')
    parser.add_argument('--cpus',
                        type=int,
                        default=1,
                        help='Number of CPUs to use (default 1)')
    return parser.parse_args()

def mosaic_region_density(x, lower, upper):
    # for an empirical distribution,
    # F_X(x) = 1/n \sum_{i=1}^n 1(X_i <= x)
    # the density in the region is F_X(upper) - F_X(lower)
    cdf_upper = np.mean(x <= upper)
    cdf_lower = np.mean(x <= lower)
    return cdf_upper - cdf_lower

def high_saf_density(X,x):
    # for an empirical distribution,
    # F_X(x) = 1/n \sum_{i=1}^n 1(X_i <= x)
    # we want to know density of region above x, which is 1 - F_X(x)
    cdf_x = np.mean(X <= x)
    return 1- cdf_x

def classify(mosaic_density, high_saf_density, mosaic_region_density_lower_bound, high_saf_density_upper_bound):
    if mosaic_density >= mosaic_region_density_lower_bound and high_saf_density <= high_saf_density_upper_bound:
        return "Mosaic"
    else:
        return "Not Mosaic"




def main():
    args = get_args()
    
    with open(args.input) as f:
        with open(args.output, 'w') as out:
            header = f.readline().strip().split('\t')
            header_out = header[:args.sample_col] + ['mosaic_region_density', 'high_saf_density', 'classification']
            header_out = ['sv_key'] + header_out
            print('\t'.join(header_out), file=out)
            for line in f:
                chrm = line.split('\t')[0]
                start = line.split('\t')[1]
                end = line.split('\t')[2]
                sv_key = f'{chrm}:{start}-{end}'
                safs = line.split('\t')[args.sample_col:]
                safs=np.array(safs).astype(float)
                mosaic_density = mosaic_region_density(safs, args.mosaic_region_saf_lower_bound, args.mosaic_region_saf_upper_bound)
                high_saf_density_value = high_saf_density(safs, args.high_saf_density_upper_bound)
                classification = classify(mosaic_density, high_saf_density_value, args.mosaic_region_density_lower_bound, args.high_saf_density_upper_bound)
                print('\t'.join([sv_key] + line.split('\t')[:args.sample_col] + [str(mosaic_density), str(high_saf_density_value), classification]) + '\n', file=out)

    

if __name__ == '__main__':
    main()
