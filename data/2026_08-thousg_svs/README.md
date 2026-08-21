The 1000 genomes SV set was downloaded and processed as written by Xincheng in the old manuscript:

```
The raw vcf was downloaded from 1KG FTP site and retained samples that only overlap with STIX-LR  index by using bcftools view -S sample_id.unique.txt --force-samples -o 1KGP.subset.vcf 1KGP_3202.gatksv_svtools_novelins.freeze_V3.wAF.vcf.gz . 
FTP: https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000G_2504_high_coverage/working/20210124.SV_Illumina_Integration/
```

I created sample_id.unique.txt by

```
index=<path to grch38 stix lr index>
cd $index
mapfile -t files < <(ls | grep ped)
echo "# files: ${files[@]}"
for f in "${files[@]}"; do tail -n +2 $f | cut -f 1 >> sample_id.txt ; done
sort sample_id.txt | uniq > sample_id.unique.txt
```
