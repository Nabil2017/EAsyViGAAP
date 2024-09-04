
 ##                                                       **EAsyViGAAP (Easy Viral Genome Assembly and Annotation Processing)**            
                     

This easy-to-use, Linux-based pipeline automates the process of genome assembly and annotation, specifically for viral genomes. 
It integrates various bioinformatics tools and scripts to perform quality control, adapter trimming, assembly, and annotation. 
The pipeline is designed to run within a specific Conda environment.
This workflow is dedicated to researchers who wish to carry out the analysis of short paired-end reads for the assembly and annotation 
of complete viral genomes. It is especially helpful for beginners in the field of bioinformatics who want to explore data analysis 
but find some tasks challenging.

### Clone the Repository:
~~~
git clone https://github.com/Nabil2017/EAsyViGAAP.git
cd EAsyViGAAP/
~~~

### Conda Install:

Make sure you have Conda installed on your system. If not, you can install it by following the instructions available in Anaconda website.

~~~
wget https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh
bash Anaconda3-2024.06-1-Linux-x86_64.sh -b
conda init
source ~/.bashrc
conda --version
~~~

### EAsyViGAAP content and Specific considerations:
~~~
main.py                               # Full run session. You need to change the file prefix with you virus name.
FastQC_analysis.py                    # To evaluate the quality of the input fastq files.
Quality_per_read.py                   # To generate plots of the quality score per reads, useful to choose the parameters to filter the reads (we choose the optimal length of 100 and quality score of 60 for the test input files).
multi_png.py                          # Combine all plots in one unique HTML file.
Trim_Adapters.py                      # To remove adapters from reads, you need a list of adapters used in your experiment saved in a text file in the RAW_DATA folder.
Pipeline_virus_assembly.py            # For the assembly of the viral genome using the parameters mentioned above, we used an optimal read length of 100 and a quality score of 60. You should adjust these values in the script as needed for 
                                      # your analysis. 
samtools.sh                           # SHELL script. If you wish to change the optimal read length, you need to replace the value 100 with the appropriate value.
samtools_mpileup.sh                   # You should change both values, 100 and 60, to your preferred settings.
process_fasta.py                      # To generate processed assembly fasta file.
reference.fa                          # These files are specific to the SARS-CoV-2 reference genome. If you wish to use a different viral reference genome, you will need to replace these files
referance.fasta                       # with the corresponding reference genome files.
RAW_DATA                              # Folder contains the input fastq files and Adapter_List.txt file (more details in Tutorial file in RAW_DATA).  
~~~

## Installation:
### Requirements:
The pipeline was optimized using the following bioinformatics tools and their respective versions. However, it should be compatible with later versions of these tools.

![pyhton version](https://img.shields.io/badge/python-v3.11.9%20-blue)
![Fastqc version](https://img.shields.io/badge/Fastqc-v0.12.1%20-blue)
![Samtools version](https://img.shields.io/badge/Samtools-v1.20%20-blue)
![Trimmomatic version](https://img.shields.io/badge/Trimmomatic-v0.39%20-blue)
![Quast version](https://img.shields.io/badge/Quast-v5.2.0%20-blue)
![Prokka version](https://img.shields.io/badge/Prokka-v1.14.6%20-blue)

![bcftools version](https://img.shields.io/badge/bcftools-v1.20%20-blue)
![Freebayes version](https://img.shields.io/badge/Freebayes-v1.3.8%20-blue)
![Biopython version](https://img.shields.io/badge/Biopython-v1.84%20-blue)
![Matplotlib version](https://img.shields.io/badge/Matplotlib-v3.9.1%20-blue)
![Bwa version](https://img.shields.io/badge/Bwa-v0.7.18%20-blue)
![Cutadapt version](https://img.shields.io/badge/Cutadapt-v4.9%20-blue)
 

### To install these dependencies:
~~~
conda env create -f EAsyViGAAP-env.yml  
~~~

### Install verifiation
~~~
python --version
fastqc --version
samtools --version
trimmomatic -version
quast --version
prokka --version
bcftools --version
freebayes --version
python -c "import Bio; print(Bio.__version__)"                     # for biopython version
python -c "import matplotlib; print(matplotlib.__version__)"       # for Matplotlib version
bwa 2>&1 | grep "Version"                                          # for bwa version
cutadapt --version
~~~

### RAW_DATA folder contains the fastq input files as well as the adapter sequences to be trimmed.
These sequences were generated using the MiSeq platform at the Laboratory of Molecular and Cellular Screening Processes, Centre of Biotechnology of Sfax, University of Sfax, as part of the ADAGE (Decision System Based on Genome Analyses in COVID-19 Tunisian Patients) project (PRFCOVID19-GP2).
The test fastq files can be downloaded from these links:
~~~
[Download file1_R1.fastq ](https://drive.google.com/file/d/1xpDPBVo6SN4QeTghRM0lG4i6xR0_ScSw/view?usp=sharing)
[Download file1_R2.fastq ](https://drive.google.com/file/d/1GytdWiHMuozmeVDPNvu3DyBiyNJSyVBB/view?usp=sharing) 
~~~

## USAGE:
### To run the entire pipeline, use the following command:
~~~
python main.py                        # If you plan to run analyses on multiple input files, consider using a High-Performance Computing (HPC) environment to efficiently handle the 
                                      # computational demands.
~~~

### Alternatively, you can run each step of the pipeline individually. 

### Output folders and files:
~~~
FASTQC_Results                        # the HTML files of quality reports as well as the quality per reads plots.
TRIMMED_DATA                          # the fastq files after trimming which will be used for assembly.
Assembly_Results                      # the assembly genome (file*_assembly.fasta).
Annotation_Results                    # the annotated genome (*.gbk).
logfile.log                           # records the execution details, errors, and other information generated by the above main script. 
~~~




