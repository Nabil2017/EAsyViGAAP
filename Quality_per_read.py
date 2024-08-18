from Bio import SeqIO
import matplotlib.pyplot as plt
import numpy as np
import os
import multiprocessing


def calculate_quality_metrics(records):
    mean_quality_per_read = [np.mean(record.letter_annotations["phred_quality"]) for record in records]
    read_lengths = [len(record) for record in records]
    return mean_quality_per_read, read_lengths


def process_file(fastq_file):

    input_file = os.path.join(input_directory, fastq_file)
    

    records = list(SeqIO.parse(input_file, "fastq"))
    mean_quality_per_read, read_lengths = calculate_quality_metrics(records)


    plt.figure(figsize=(10, 5))
    plt.scatter(read_lengths, mean_quality_per_read)
    plt.title("Mean Quality Score per Read Length for " + fastq_file)
    plt.xlabel("Read Length")
    plt.ylabel("Mean Quality Score")
    plt.grid(True)


    output_file = os.path.join(output_directory, fastq_file.replace(".fastq", "_quality_per_read_length.png"))
    

    plt.savefig(output_file)


    plt.close()


input_directory = "RAW_DATA"
output_directory = "FASTQC_Results"


if not os.path.exists(output_directory):
    os.makedirs(output_directory)


fastq_files = [f for f in os.listdir(input_directory) if f.endswith(".fastq")]


num_processes = multiprocessing.cpu_count()


with multiprocessing.Pool(processes=num_processes) as pool:
    pool.map(process_file, fastq_files)

