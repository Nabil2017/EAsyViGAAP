
 ##                                                       **EAsyViGAAP (Easy Viral Genome Assembly and Annotation Processing)**            
                     

This easy-to-use, Linux-based pipeline automates the process of genome assembly and annotation, specifically for viral genomes. 
It integrates various bioinformatics tools and scripts to perform quality control, adapter trimming, assembly, and annotation. 
The pipeline is designed to run within a specific Conda environment.

## Installation:

### Prerequisites:
Conda: Make sure you have Conda installed on your system. If not, you can install it by following the instructions available in Anaconda website.

~~~
wget https://repo.anaconda.com/archive/Anaconda3-latest-Linux-x86_64.sh
chmod +x Anaconda3-latest-Linux-x86_64.sh
./Anaconda3-latest-Linux-x86_64.sh
conda init
source ~/.bashrc
conda --version
~~~
## Clone the Repository:
~~~
git clone https://github.com/Nabil2017/EAsyViGAAP.git
cd EAsyViGAAP/
~~~
## EAsyViGAAP content and Specific considerations:
~~~
FastQC_analysis.py                    # Quality Control script to evaluate the input fastq files.
process_fasta.py                      # To generate quality plots.
Quality_per_read.py                   # Plot analysis of the quality score per reads, useful to choose the parameters to filter the reads (we choose the optimal length of 100 and quality score of 60 for the test input files).
multi_png.py                          # combine all plots in a unique HTML file.
Trim_Adapters.py                      # to clean adapters from reads. it requires a list of adapters used in your exeriment and saved in a text file in the RAW_DATA folder.
Pipeline_virus_assembly.py            # for the assembly of the viral genome using the above parameters. We used optimal read length 100 and quality score of 60 . You should change these values in the script as you see suitable for your 
                                      # analysis. 
samtools.sh                           # SHELL script. If you wish to change the optimal read lenght, you need to change 100 by the suitable value.
samtools_mpileup.sh                   # you should change the two values 100 and 60 as you like.
reference.fa                          # These files are for the SARS-CoV-2 reference genome. If you wish to use a different viral reference genome,  
referance.fasta                       # you will need to replace these files with the corresponding reference genome files for your selected virus.
~~~
### conda 24.7.1 was used to install the pipeline dependencies.

## Requirements:
The pipeline was optimized using the following bioinformatics tools and their respective versions. However, it should be compatible with later versions of these tools.
~~~
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
~~~
### To install these dependencies, open a terminal and navigate to the EAsyViGAAP directory:
~~~
conda create --name genomics-env      # create genomics-env
conda activate genomics-env           # activate genomics-env
pip install -r INSTALL.txt            # install dependencies. Be sure you have pip installed, otherwise: conda install pip
~~~

### RAW_DATA folder contains the fastq input files as well as the adapter sequences to be trimmed.

## USAGE:
### To run the entire pipeline, use the following command:
~~~
python main.py                        # If you plan to run analyses on multiple input files, consider using a High-Performance Computing (HPC) environment to efficiently handle the computational demands.
~~~

### Alternatively, you can run each step of the pipeline individually.

## Output folders and files:
~~~
FASTQC_Results                        # the HTML files of quality reports as well as the quality per reads plots.
TRIMMED_DATA                          # the fastq files after trimming which will be used for assembly.
Assembly_Results                      # the assembly genome (file*_assembly.fasta).
Annotation_Results                    # the annotated genome (*.gbk).
~~~




