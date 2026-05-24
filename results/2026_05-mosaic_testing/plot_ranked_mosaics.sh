#!/usr/bin/env bash

join_script='/data/jake/rl-tools/wrangle/join.py'
outfile_data='mosaic_rank.plot_data.tsv'
mosaic_saf='./te_mosaic.saf.keyed.tsv'
mosaic_rank='./mosaic_rank.tsv'
plot_script=hist.py


# high ranking mosaics
tmp1_in=$(mktemp --suffix=.tsv)
tmp1_out=$(mktemp --suffix=.tsv)
trap "rm -f $tmp1_in $tmp1_out" EXIT
sed -n '1,3p' "$mosaic_rank" > "$tmp1_in"
"$join_script" \
    -x "$tmp1_in" \
    -y "$mosaic_saf" \
    --keys sv_key \
    --type left \
    --output "$tmp1_out"

# low ranking mosaics
tmp2_in=$(mktemp --suffix=.tsv)
tmp2_out=$(mktemp --suffix=.tsv)
trap "rm -f $tmp2_in $tmp2_out" EXIT
head -n 1 "$mosaic_rank" > "$tmp2_in"
tail -n 2 "$mosaic_rank" >> "$tmp2_in"
"$join_script" \
    -x "$tmp2_in" \
    -y "$mosaic_saf" \
    --keys sv_key \
    --type left \
    --output "$tmp2_out"

# combine
cat "$tmp1_out" <(tail -n +2 "$tmp2_out") > "$outfile_data"

# plot
rm tmp.out || echo "No tmp.out to remove"
while IFS=$'\t' read -r -a fields; do
    sv_id="${fields[0]}"
    sv_id=$(printf '%s' "$sv_id" | sed 's/:/-/g')
    echo "# svid: $sv_id"
    min_ks="${fields[1]}"
    printf '%s\n' "${fields[@]:6}" | \
        awk '$0 < 3' | \
        $plot_script \
            --annotate "0.4:0.7:SV=$sv_id:black,0.4:0.5:minKS=$min_ks:black" -o "mosaic_${sv_id}.png" \
            -x SAF -y Freq --x_min -0.05 --bins 10 --ylog --x_max 3
done < <(tail -n +2 "$outfile_data")
