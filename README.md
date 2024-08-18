*********************************************************EAsyViGAAP*****************************************

This easy-to-use linux-based pipeline automates the process of genome assembly and annotation, specifically for viral genomes.
It integrates various bioinformatics tools and scripts to perform quality control, adapter trimming, 
assembly, and annotation. The pipeline is designed to run in a specific Conda environment.


# Installation:

Prerequisites:
Conda: Make sure you have Conda installed on your system. If not, you can install it by following the instructions available in Anaconda website.

wget https://repo.anaconda.com/archive/Anaconda3-latest-Linux-x86_64.sh
chmod +x Anaconda3-latest-Linux-x86_64.sh
./Anaconda3-latest-Linux-x86_64.sh
conda init
source ~/.bashrc
conda --version   # to get your conda version

## conda 24.7.1 was used to install the pipeline dependencies.

# Requirements:
The pipeline was optimized with the following bioinformatics tools and versions; however, it should work with later released versions.

FastQC==0.12.1
samtools==1.20
trimmomatic==0.39
bwa==0.7.18-r1243-dirty
quast==5.2.0
prokka==1.14.6
bcftools==1.20
freebayes==1.0.0
biopython==1.84
matplotlib==3.9.1
python==3.11

# To install these dependencies, open a terminal and navigate to the EAsyViGAAP directory:
conda create --name genomics-env      # create genomics-env
conda activate genomics-env           # activate genomics-env
pip install -r INSTALL.txt            # install dependencies. Be sure you have pip installed, otherwise: conda install pip

# The EAsyViGAAP directory include several python and Shell scripts as well as two fasta files for reference genome:
reference.fa                          # these two files for SARS-CoV-2 reference genome, so if you wish to include different viral reference genome you need to replace these files by the 
referance.fasta                       # corresponding viral reference genome.

# RAW_DATA folder contains the fastq input files as well as the adapter sequences to be trimmed.

# To run the entire pipeline, use the following command:
python main.py                        # if you wish to run multiple input files, you should think to use HPC.

# Alternatively, you can run each step of the pipeline individually.
# Output folders and files:
FASTQC_Results                        # the HTML files of quality reports as well as the quality per reads plots.
TRIMMED_DATA                          # the fastq files after trimming which will be used for assembly.
Assembly_Results                      # the assembly genome (file*_assembly.fasta).
Annotation_Results                    # the annotated genome (*.gbk).




