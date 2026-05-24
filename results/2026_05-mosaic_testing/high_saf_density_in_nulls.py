#!/usr/bin/env python3

import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--input", '-i', help='csv string of null files',
    default='null_het.npy,null_ref.npy')
parser.add_argument("--output", '-o', default='high_saf_density_in_nulls.png')
parser.add_argument("--saf_upper", type=float, default=0.5)

def high_saf_density(X,x):
    # for an empirical distribution,
    # F_X(x) = 1/n \sum_{i=1}^n 1(X_i <= x)
    # we want to know density of region above x, which is 1 - F_X(x)
    cdf_x = np.mean(X <= x)
    return 1- cdf_x

def combine_nulls(nulls):
    return np.concatenate(nulls)

def plot_densities(densities, output, saf_upper):
    labels, density_values = zip(*densities)
    bars = plt.bar(labels, density_values)
    for bar, value in zip(bars, density_values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.7f}",
            ha="center",
            va="bottom",
        )
    plt.ylabel("Density in high SAF region")
    plt.title(f"Density of nulls in high SAF region (> {saf_upper})")
    plt.savefig(output)

def main():
    args = parser.parse_args()
    nulls = {}
    print("# reading nulls", args.input)
    null_files = args.input.split(",")
    for null_file in null_files:
        nulls[null_file] = np.load(null_file)
    nulls['combined'] = combine_nulls(list(nulls.values()))
    print("# computing density in high SAF regions")
    densities = []
    for null_file, null in nulls.items():
        density = high_saf_density(null, args.saf_upper)
        print(f"# {null_file}: density in high SAF region = {density}")
        densities.append((null_file, density))
    print("# plotting densities")
    plot_densities(densities, args.output, args.saf_upper)


if __name__ == "__main__":
    main()

