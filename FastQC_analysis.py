import os
import subprocess
import zipfile
import time
import sys
from concurrent.futures import ThreadPoolExecutor
from Bio import SeqIO
from statistics import mean, median
import matplotlib.pyplot as plt

try:
    from Bio import SeqIO
except ImportError:
    print("Biopython is not installed. Installing Biopython...")
    subprocess.run([sys.executable, "-m", "pip", "install", "biopython"])

input_directory = "RAW_DATA"
output_directory = "FASTQC_Results"

os.makedirs(output_directory, exist_ok=True)

fastq_files = [filename for filename in os.listdir(input_directory) if filename.endswith(".fastq")]

processed_files = set()
quality_assessments = []

def analyze_fastq(file):
    file_path = os.path.join(input_directory, file)

    if file in processed_files:
        print(f"Skipping {file} - Already processed.")
        return

    subprocess.run(["fastqc", "--threads", "4", file_path, "--outdir", output_directory])

    file_output_directory = os.path.join(output_directory, file.replace(".fastq", "_fastqc"))
    zip_filename = os.path.join(file_output_directory, "fastqc.zip")
    summary_filename = os.path.join(file_output_directory, "summary.txt")

    timeout = time.time() + 30
    while not os.path.exists(zip_filename) and time.time() < timeout:
        time.sleep(1)

    if os.path.exists(zip_filename):
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(file_output_directory)

        if os.path.exists(summary_filename):
            with open(summary_filename, 'r') as output_file:
                for line in output_file:
                    if line.startswith("Filename"):
                        filename = line.split("\t")[1].strip()
                    elif line.startswith("Total Sequences"):
                        total_sequences = line.split("\t")[1].strip()
                    elif line.startswith("Sequence length"):
                        seq_length = line.split("\t")[1].strip()
                    elif line.startswith("%GC"):
                        gc_content = line.split("\t")[1].strip()

                print(f"File: {filename}\nTotal Sequences: {total_sequences}\nSequence Length: {seq_length}\n%GC Content: {gc_content}\n" + "=" * 40)
        else:
            print(f"FastQC analysis for {file} was not successful.")

    with open(file_path, "r") as handle:
        total_reads = 0
        total_bases = 0
        per_base_quality_scores = []

        for record in SeqIO.parse(handle, "fastq"):
            total_reads += 1
            total_bases += len(record.seq)
            per_base_quality_scores.extend(record.letter_annotations["phred_quality"])

        if total_reads > 0:
            average_read_length = total_bases / total_reads
            average_phred_score = mean(per_base_quality_scores)
            median_quality = median(per_base_quality_scores)
            min_quality = min(per_base_quality_scores)

            assessment = {
                "File": file,
                "Total Reads": total_reads,
                "Total Bases": total_bases,
                "Average Read Length": average_read_length,
                "Average Phred Score": average_phred_score,
                "Median Quality Score": median_quality,
                "Minimum Quality Score": min_quality
            }

            quality_assessments.append(assessment)

with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(analyze_fastq, fastq_files)

for file in fastq_files:
    file_path = os.path.join(input_directory, file)
    output_figure_path = os.path.join(output_directory, f"{file}_read_size_distribution.png")

    with open(file_path, "r") as handle:
        read_lengths = [len(record.seq) for record in SeqIO.parse(handle, "fastq")]

    plt.figure(figsize=(10, 6))
    plt.hist(read_lengths, bins=50, color='blue', alpha=0.7)
    plt.title(f'Read Size Distribution for {file}')
    plt.xlabel('Read Length')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig(output_figure_path)
    plt.close()

output_file_path = os.path.join(output_directory, "table.txt")
with open(output_file_path, "w") as output_file:
    output_file.write("\nQuality Assessments:\n")
    output_file.write("=" * 80 + "\n")
    output_file.write("{:<20} {:<15} {:<15} {:<20} {:<20} {:<20} {:<20}\n".format(
        "File", "Total Reads", "Total Bases", "Average Read Length",
        "Average Phred Score", "Median Quality Score", "Minimum Quality Score"
    ))
    output_file.write("=" * 80 + "\n")

    for assessment in quality_assessments:
        output_file.write("{:<20} {:<15} {:<15} {:<20.2f} {:<20.2f} {:<20} {:<20}\n".format(
            assessment["File"], assessment["Total Reads"], assessment["Total Bases"],
            assessment["Average Read Length"], assessment["Average Phred Score"],
            assessment["Median Quality Score"], assessment["Minimum Quality Score"]
        ))

    output_file.write("=" * 80 + "\n")

print(f"Quality assessment table written to {output_file_path}")

