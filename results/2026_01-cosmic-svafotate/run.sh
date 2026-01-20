#!/usr/bin/env bash
# run conda activate svafotate-env first
../../src/svafotate-hg002_cmrg.py \
  --input ../2026_01-cosmic-tsv-to-vcf/cosmic.v103.grch38.vcf \
  --outdir $(pwd) \
  --bed "$SVAFOTATE_BED" \
  --env_name svafotate-env \
  --timefile ../2026_01-cosmic-svafotate/svafotate_cosmic.times \
  --outfile ../2026_01-cosmic-svafotate/svafotate-cosmic