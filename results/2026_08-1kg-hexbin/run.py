#!/usr/bin/env python3
import argparse
import pandas as pd
import subprocess
parser = argparse.ArgumentParser()
parser.add_argument("--input", default="../2026_08-frequency_benchmark_summary/thousg-merge.tsv")
parser.add_argument("--output_stix_v_thousg", default="hexbin-stixlr_mr5-thousg.png")
parser.add_argument("--output_stix_v_needlr", default="hexbin-stixlr_mr5-needlr.png")
args = parser.parse_args()

COL_STIX='stix_samples_mr5'
COL_THOUSG_AF='thousg_af'
COL_NEEDLR_AF='needlr_af_ov05'
COLOR="Reds"

def hex_plot(
    path_stix,
    path_other: str,
    path_out: str,
    color: str,
    xlabel: str,
    ylabel: str,
    title: str,
    path_merged_out: str,
    height: int = 4,
    width: int = 5,
):
    cmd = f"./hex_plot.py --stix {path_stix} --other {path_other} "
    cmd += f"--output {path_out} --color {color} --height {height} "
    cmd += f"--width {width} --xlabel '{xlabel}' --ylabel '{ylabel}' "
    cmd += f"--title '{title}' --merged {path_merged_out}"
    result = subprocess.run(cmd, shell=True, check=True)
    return result.returncode


def main():
    df = pd.read_csv(args.input,sep="\t")
    df_stix = df[['svid', COL_STIX]]
    df_stix.to_csv('stix.tsv',sep='\t',index=False)
    df_thousg = df[['svid', COL_THOUSG_AF]]
    df_thousg.to_csv('thousg.tsv',sep='\t',index=False)
    df_needlr = df[['svid', COL_NEEDLR_AF]]
    df_needlr.to_csv('needlr.tsv',sep='\t',index=False)
    # stix v 1kg
    hex_plot(
        "stix.tsv",
        "thousg.tsv",
        args.output_stix_v_thousg,
        COLOR,
        "1KG AF",
        "Num. of samples with STIX long-read depth >= 5",
        "1KG germline SVs",
        "stixlr-v-thousg.tsv"
    )
    hex_plot(
        "stix.tsv",
        "needlr.tsv",
        args.output_stix_v_needlr,
        COLOR,
        "NeedLR;OV=0.5 AF",
        "Num. of samples with STIX long-read depth >= 5",
        "1KG germline SVs",
        "stixlr-v-needlr.tsv"
    )

if __name__=="__main__":
    main()