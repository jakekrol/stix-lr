import argparse
import sys
import numpy as np
from scipy.stats import ks_2samp, gaussian_kde
from multiprocessing import Pool


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i',
                        type=str,
                        required=True,
                        help='te_mosiac_agg.allele_ballance.lessmd.rm_missing.tsv')
    parser.add_argument('--nulls', '-n',
                        type=str,
                        nargs='+',
                        required=True,
                        help='One or more .npy null distributions')
    parser.add_argument('--sample-col',
                        type=int,
                        default=4,
                        help='First column index of per-sample values (default 4)')
    parser.add_argument('--n-boot',
                        type=int,
                        default=100,
                        help='Bootstrap iterations (default 100)')
    parser.add_argument('--seed',
                        type=int,
                        default=0,
                        help='Random seed')
    parser.add_argument('--query_lower_bound',
                        type=float,
                        default=-1.0)
    parser.add_argument('--query_upper_bound',
                        type=float,
                        default=1e6)
    parser.add_argument('--output', '-o',
                        type=str)
    parser.add_argument('--cpus',
                        type=int,
                        default=1,
                        help='Number of CPUs to use (default 1)')
    return parser.parse_args()


def process_mosaic(args_tuple):
    """Process a single mosaic line in parallel."""
    line, nulls_dict, sample_col, n_boot, seed, lower_bound, upper_bound = args_tuple
    
    fields = line.rstrip('\n').split('\t')
    chrom, star, end = fields[:3]
    sv_key = f'{chrom}:{star}-{end}'
    
    results_dict = {}
    raw = fields[sample_col:]
    query = np.array([float(v) for v in raw if v not in ('', 'NA')])
    query = query[(query > lower_bound) & (query <= upper_bound)]
    
    if len(query) < 2:
        return sv_key, None  # Skip if insufficient data
    
    rng = np.random.default_rng(seed)
    
    # for each null dist
    for path, null in nulls_dict.items():
        ks_values = []
        # downsample and compute KS stat
        for _ in range(n_boot):
            sample = rng.choice(null, size=len(query), replace=True)
            ks, _ = ks_2samp(query, sample)
            ks_values.append(ks)
        ks_avg = np.mean(ks_values)
        results_dict[path] = ks_avg
    
    # compute min KS across all nulls
    min_ks = min(results_dict.values())
    results_dict['min_ks'] = min_ks
    
    return sv_key, results_dict


def main():
    args = get_args()
    
    nulls = {path: np.load(path) for path in args.nulls}
    
    # gather queries
    with open(args.input) as f:
        n_lines = sum(1 for _ in f) - 1  # exclude header
        f.seek(0)
        f.readline()  # skip header
        lines = [line for line in f]
    
    print(f"# processing {n_lines} SV queries with {args.cpus} CPUs", file=sys.stderr)
    
    # prep args for parallel query processing
    process_args = [
        (line, nulls, args.sample_col, args.n_boot, args.seed + i, 
         args.query_lower_bound, args.query_upper_bound)
        for i, line in enumerate(lines)
    ]
    
    # score all queries
    results = {}
    with Pool(args.cpus) as pool:
        results_list = pool.map(process_mosaic, process_args)
    
    # collect results
    for sv_key, result_dict in results_list:
        if result_dict is not None:
            results[sv_key] = result_dict
    
    # sort by minimum KS stat (descending)
    sorted_keys = sorted(results.keys(), key=lambda k: results[k]['min_ks'], reverse=True)
    
    with open(args.output, 'w') as out:
        print("sv_key\tmin_ks", file=out)
        for key in sorted_keys:
            print(key, results[key]['min_ks'], sep='\t', file=out)
    
    print(f"# Processed {len(results)} mosaics, wrote to {args.output}", file=sys.stderr)


if __name__ == '__main__':
    main()
