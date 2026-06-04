#!/usr/bin/env python3

import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--input", '-i', help='csv string of null files',
    default='null_het.npy,null_ref.npy')
parser.add_argument("--output", '-o', default='mosaic_density_in_nulls.png')
parser.add_argument("--mosaic_region_lower", type=float, default=0.05)
parser.add_argument("--mosaic_region_upper", type=float, default=0.45)

def mosaic_region_density(x, lower, upper):
    # for an empirical distribution,
    # F_X(x) = 1/n \sum_{i=1}^n 1(X_i <= x)
    # the density in the region is F_X(upper) - F_X(lower)
    cdf_upper = np.mean(x <= upper)
    cdf_lower = np.mean(x <= lower)
    return cdf_upper - cdf_lower

def combine_nulls(nulls):
    return np.concatenate(nulls)

def plot_densities(densities, output, lower, upper):
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
    plt.ylabel("Density in mosaic region")
    plt.title(f"Density of nulls in mosaic region [{lower}, {upper}]")
    plt.savefig(output)

def main():
    args = parser.parse_args()
    nulls = {}
    print("# reading nulls", args.input)
    null_files = args.input.split(",")
    for null_file in null_files:
        nulls[null_file] = np.load(null_file)
    nulls['combined'] = combine_nulls(list(nulls.values()))
    print("# computing density in mosaic regions")
    densities = []
    for null_file, null in nulls.items():
        density = mosaic_region_density(null, args.mosaic_region_lower, args.mosaic_region_upper)
        print(f"# {null_file}: density in mosaic region = {density}")
        densities.append((null_file, density))
    print("# plotting densities")
    plot_densities(densities, args.output, args.mosaic_region_lower, args.mosaic_region_upper)


if __name__ == "__main__":
    main()

