#!/usr/bin/env bash

pairs=$1
pd=$2
out=$3
study=$4
spath=`dirname $0`
# find tumor bams from pair list
cut -f 2 $pairs | sort | uniq | xargs -IBN find $pd/ALIGN/BN/BAM -name '*.merged.final.ba*' > bam_list.txt
# find normal bams and append to list
cut -f 3 $pairs | sort | uniq | xargs -IBN find $pd/ALIGN/BN/BAM -name '*.merged.final.ba*' >> bam_list.txt
# find tumor fastqs from pair list
cut -f 2 $pairs | sort | uniq | xargs -IBN find $pd/RAW/BN -name '*_sequence.txt.gz' > fq_list.txt
# find normal fastqs and append
cut -f 3 $pairs | sort | uniq | xargs -IBN find $pd/RAW/BN -name '*_sequence.txt.gz' >> fq_list.txt
# find anaylsis files
cut -f 1 $pairs | sort | uniq | xargs -IBN find $pd/ANALYSIS/BN -name 'somatic.indel.vcf' > analysis_files.txt
cut -f 1 $pairs | sort | uniq | xargs -IBN find $pd/ANALYSIS/BN -name 'BN.vcf.keep' >> analysis_files.txt
cut -f 1 $pairs | sort | uniq | xargs -IBN find $pd/ANALYSIS/BN -name 'BN.out.keep' >> analysis_files.txt
cut -f 3 $pairs | sort | uniq | xargs -IBN find $pd/ANALYSIS/BN -name '*.germline_pass.vcf' >> analysis_files.txt
# find annotation files
cut -f 1 $pairs | sort | uniq | xargs -IBN find $pd/ANNOTATION/BN -name '*.snv.vep*.vcf' > annotation_files.txt
cut -f 1 $pairs | sort | uniq | xargs -IBN find $pd/ANNOTATION/BN -name '*.xls' >> annotation_files.txt
cut -f 1 $pairs | sort | uniq | xargs -IBN find $pd/ANNOTATION/BN -name '*.somatic.indel.vep*.vcf' >> annotation_files.txt
cut -f 3 $pairs | sort | uniq | xargs -IBN find $pd/ANNOTATION/BN -name '*.germline*.vep*.vcf' >> annotation_files.txt
cut -f 3 $pairs | sort | uniq | xargs -IBN find $pd/ANNOTATION/BN -name '*.germline*.xls' >> annotation_files.txt
# cat all files
cat analysis_files.txt annotation_files.txt bam_list.txt  fq_list.txt > $out\_to_upload.txt
# prep upload list using helper script
# study, like CPCI_Retrospective_Study
$spath/upload_files.py pro_to_upload.txt '$pd/' $study
# hammer amazon
# mv flist.txt $out\_flist.txt
# cat $out\_flist.txt | xargs -IFN -P 4 sh -c 'aws s3 cp FN --sse --profile tempus' 2> $out\_cp.log >> $out\_cp.log &