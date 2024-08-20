#! /bin/sh

file_name=$1
samtools sort -n $file_name.sam | samtools fixmate -m -O bam - $file_name.fixmate.bam
samtools view -h $file_name.fixmate.bam | awk 'length($10) > 100 || $1 ~ /^@/' | samtools view -bS - > $file_name.fixmate.100.bam #It keeps reads that have a sequence length greater than 100
samtools sort $file_name.fixmate.100.bam -o $file_name.fixmate.100.ref.bam --reference reference.fa
samtools index $file_name.fixmate.100.ref.bam


