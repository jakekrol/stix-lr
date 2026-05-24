#!/usr/bin/env python

import pandas as pd

data_dir="../../data/2026_04-mosaic_ryan"
mosaic_saf=f"{data_dir}/te_mosiac_agg.allele_ballance.lessmd.rm_missing.tsv"

df_mosaic = pd.read_csv(mosaic_saf, sep='\t', header=0)

df_mosaic.rename(columns={df_mosaic.columns[0]: 'chrm'}, inplace=True)
df_mosaic.fillna(0, inplace=True)
df_mosaic['sv_key'] = df_mosaic.apply(lambda row: f"{row['chrm']}:{row['start']}-{row['end']}", axis=1)
cols = df_mosaic.columns.tolist()
cols = cols[-1:] + cols[:-1]
df_mosaic = df_mosaic[cols]
df_mosaic.to_csv("te_mosaic.saf.keyed.tsv", sep='\t', index=False)
