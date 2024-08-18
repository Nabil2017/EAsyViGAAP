#! /bin/sh
file_name=$1
bcftools mpileup -f reference.fasta $file_name.fixmate.100.q60.ref.bam | bcftools call -c | vcfutils.pl vcf2fq > $file_name.fasta



