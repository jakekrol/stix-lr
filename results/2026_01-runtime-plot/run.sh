#!/usr/bin/env bash

set -euo pipefail

all_runtimes=runtimes.tsv
if [ -f $all_runtimes ]; then
    rm $all_runtimes
fi

## cosmic
# cosmic_stixlr=
cosmic_needlr=../2026_01-cosmic-needlr/needLR_run_time.tsv
sed 's|^|cosmic_needLR\t|' $cosmic_needlr > cosmic_needlr.time
cosmic_svafotate=../2026_01-cosmic-svafotate/svafotate_cosmic.times
sed 's|^|cosmic_svafotate\t|' $cosmic_svafotate > cosmic_svafotate.time
## hg002 cmrg
hg002_stixlr=../2025_12-hg002_cmrg-stix_lr/stix_lr_hg002_cmrg_times.txt
sed 's|^|hg002_stixLR\t|' $hg002_stixlr > hg002_stixlr.time
hg002_needlr=../2026_01-hg002-needlr/needLR_run_time.tsv
sed 's|^|hg002_needLR\t|' $hg002_needlr > hg002_needlr.time
hg002_svafotate=../2025_12-hg002_cmrg-svafotate/svafotate_hg002_cmrg.times
sed 's|^|hg002_svafotate\t|' $hg002_svafotate > hg002_svafotate.time

## colo
colo_stixlr=../2026_01-colo_filt-stix_lr-rerun/stix_lr-colo.times
sed 's|^|colo_stixLR\t|' $colo_stixlr > colo_stixlr.time
colo_needlr=../2026_01-colo-needlr/needLR_run_time.tsv
sed 's|^|colo_needLR\t|' $colo_needlr > colo_needlr.time
colo_svafotate_germline=../2026_01-colo-svafotate-filt-rerun/svafotate_germline.time
sed 's|^|colo_svafotate_germline\t|' $colo_svafotate_germline > colo_svafotate_germline.time
colo_svafotate_somatic=../2026_01-colo-svafotate-filt-rerun/svafotate_somatic.time
sed 's|^|colo_svafotate_somatic\t|' $colo_svafotate_somatic > colo_svafotate_somatic.time

for f in $(ls *.time); do
    cat $f >> $all_runtimes
done

python - <<EOF
import pandas as pd
f = "$all_runtimes"
def get_dataset(x):
    x=x.lower()
    if 'colo' in x:
        return 'COLO'
    elif 'cosmic' in x:
        return 'COSMIC'
    elif 'hg002' in x:
        return 'HG002 CMRG'
    else:
        return 'unknown'
def get_method(x):
    x=x.lower()
    if 'stix' in x:
        return 'STIX-LR'
    elif 'needlr' in x:
        return 'needLR'
    elif 'svafotate' in x:
        return 'SVAFotate'
    else:
        return 'unknown'
def get_overlap_param(x):
    x=x.lower()
    if 'ov0.5' in x or 'overlap_0.5' in x:
        return '0.5'
    elif 'ov0.6' in x or 'overlap_0.6' in x:
        return '0.6'
    elif 'ov0.7' in x or 'overlap_0.7' in x:
        return '0.7'
    elif 'ov0.8' in x or 'overlap_0.8' in x:
        return '0.8'
    elif 'ov0.9' in x or 'overlap_0.9' in x:
        return '0.9'
    else:
        return ''
def get_min_reads_param(x):
    x=x.lower()
    if 'min_read_1' in x:
        return '1'
    elif 'min_read_5' in x:
        return '5'
    else:
        return ''
def get_germline_somatic_param(x):
    x=x.lower()
    if 'germline' in x:
        return 'germline'
    elif 'somatic' in x:
        return 'somatic'
    else:
        return ''
df = pd.read_csv(f, sep='\t', header=None)
df.columns = ['data','filename', 'runtime']
# assign dataset
df['dataset'] = df['data'].apply(get_dataset)
df['germline_somatic_param'] = df['filename'].apply(get_germline_somatic_param)
# try data column if filename doesn't have germline/somatic info
df.loc[df['germline_somatic_param']=='', 'germline_somatic_param'] = df.loc[df['germline_somatic_param']=='', 'data'].apply(get_germline_somatic_param)
# combine dataset and germline/somatic param if applicable
df['dataset'] = df.apply(lambda row: f"{row['dataset']}|{row['germline_somatic_param']}" if row['germline_somatic_param'] != '' else row['dataset'], axis=1)
# assign method
df['method'] = df['data'].apply(get_method)
# assign parameters
# overlap param for svafotate
df['overlap_param'] = df['filename'].apply(get_overlap_param)
# min reads param for stix-lr
df['min_reads_param'] = df['filename'].apply(get_min_reads_param)
# combine method and param if applicable
df['method'] = df.apply(lambda row: f"{row['method']};OV={row['overlap_param']}" if row['overlap_param'] != '' and row['method'] == 'SVAFotate' else row['method'], axis=1)
df['method'] = df.apply(lambda row: f"{row['method']};MR={row['min_reads_param']}" if row['min_reads_param'] != '' and row['method'] == 'STIX-LR' else row['method'], axis=1)
# clean up runtime column
df['runtime'] = df['runtime'].str.replace('seconds','').str.strip().astype(float).round(0)
# combine dataset and method for final output
df['dataset_method'] = df['dataset'] + '|' + df['method']
#lower case
df['dataset_method'] = df['dataset_method'].str.lower()
df = df[['dataset_method','runtime']]
# sort by dataset and method
df = df.sort_values(by=['runtime'])
df.to_csv(f, sep='\t', index=False)
EOF


python plot_runtimes_3panel.py \
    --input "$all_runtimes" \
    --output runtimes.png