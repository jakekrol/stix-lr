# STIX-LR analyses

- [Benchmark summary](results/2026_08-frequency_benchmark_summary)
- [1kg hexbin](results/2026_08-1kg-hexbin)
- [COSMIC density](results/2026_01-cosmic-density)
- [COSMIC hexbin](results/2026_08-cosmic-hexbin)
- [COLO ROC](results/2026_08-colo-roc)
- [COLO fraction of germline SVs with 0 pop. freq](results/2026_08-colo-roc)
- [HG002 hexbin](results/2026_08-hg002_cmrg-hexbin)
- [HG002 type and length](results/2026_08-hg002-missed)
- [HG002 CMRG density](results/2026_01-hg002_cmrg-density)
- [HG002 CMRG hexbin](results/2026_08-hg002_cmrg-hexbin)
- [HG002 CMRG type and length](results/2026_08-hg002_cmrg-missed)

## 1kg

Hexbin STIX-LR (min. reads = 5) v needLR (overlap=0.5)
![](results/2026_08-1kg-hexbin/hexbin-stixlr_mr5-needlr_af_ov0.5.png)

## COSMIC

Hexbin STIX-LR (min. reads = 5) v needLR (overlap=0.5)
![](results/2026_08-cosmic-hexbin/hexbin-stixlr_mr5-needlr_af_ov0.5.png)

Hexbin STIX-LR (min. reads = 5) v SVAFotate (overlap = 0.9)
![](results/2026_08-cosmic-hexbin/hexbin-stixlr_mr5-svafotate_ov0.9.png)

Number of SVs with 0 pop. freq
![](results/2026_01-cosmic-density/cosmic-sv-popfreq-density_bar.png)

Density distribution of pop. freq > 0
![](results/2026_01-cosmic-density/cosmic-sv-popfreq-density_violin.png)

## COLO

Somatic SV classification
![](results/2026_08-colo-roc/colo-stix_lr-svafotate-need_lr-new_roc.png)

Fraction of missed germline variants
![](results/2026_08-colo-roc/bar-missed_germlines.png)

## HG002

Hexbin STIX-LR (min. reads = 5) v needLR (overlap=0.5)
![](results/2026_08-hg002-hexbin/hexbin-stixlr_mr5-needlr_af_ov0.5.png)

Hexbin STIX-LR (min. reads = 5) v SVAFotate (overlap=0.9)
![](results/2026_08-hg002-hexbin/hexbin-stixlr_mr5-svafotate_ov0.9.png)

## HG002 CMRG

Hexbin 
![](results/2026_08-hg002_cmrg-hexbin/combined-hexbin-stixlr-needlr.png)
![](results/2026_08-hg002_cmrg-hexbin/combined-hexbin-stixlr-svafotate.png)

Density
![](results/2026_01-hg002_cmrg-density/hg002-cmrg-popfreq-density.png)

## Population/allele frequency bins
![](results/2026_08-frequency_benchmark_summary/cosmic-freq_bin.png)
![](results/2026_08-frequency_benchmark_summary/1kg-freq_bin.png)
![](results/2026_08-frequency_benchmark_summary/colo_germline-freq_bin.png)
![](results/2026_08-frequency_benchmark_summary/hg002-freq_bin.png)
![](results/2026_08-frequency_benchmark_summary/hg002cmrg-freq_bin.png)
![](results/2026_08-frequency_benchmark_summary/colo_somatic-freq_bin.png)



