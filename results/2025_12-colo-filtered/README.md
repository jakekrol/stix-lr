# goal
- somatic colo829 vcf had 0/0 genotypes to filter
- merge file may contain somatic + germline. want to separate out germline only

## details
- see `run.sh` for processing
- see `colo_germline.vcf` for decoupled somatic svs from merge file

## use
- for somatic classification task
    - filter out somatic_merge_ids.txt from merge/benchmark results.
    - remove colo829_somatic_grch38_gt00_ids.txt from somatic results.
