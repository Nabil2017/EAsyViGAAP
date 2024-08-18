import os
import subprocess
import glob
from multiprocessing import Pool
import logging


log_file = "logfile.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


raw_data_dir = "TRIMMED_DATA"


file_pattern = os.path.join(raw_data_dir, "file*_R*.fastq")


file_paths = sorted(glob.glob(file_pattern))


def process_file(file_path):

    file_name = os.path.splitext(os.path.basename(file_path))[0]


    underscore_index = file_name.index("_", 4)


    file_name = file_name[:underscore_index]
    logging.info("Processing file: %s", file_path)


    reference_path = os.path.join("reference.fa")
    if not os.path.exists(reference_path + ".bwt"):
        logging.info("Running bwa index")
        with open(log_file, "a") as log:
            subprocess.call(["bwa", "index", reference_path], stdout=log, stderr=log)


    logging.info("Running bwa mem")
    with open(log_file, "a") as log:
        subprocess.call(
            ["bwa", "mem", reference_path, os.path.join(raw_data_dir, file_name + "_R1.fastq"), os.path.join(raw_data_dir, file_name + "_R2.fastq")],
            stdout=open(file_name + ".sam", "w"),
            stderr=log
        )


    subprocess.call(["sh", "samtools.sh", file_name])


    subprocess.call(["bamtools", "index", "-in", file_name + ".fixmate.100.ref.bam"])


    with open(file_name + ".freebayes.100.ref.vcf", "w") as vcf_file, open(log_file, "a") as log:
         subprocess.call(["freebayes", "-p", "1", "-f", reference_path, file_name + ".fixmate.100.ref.bam"],
                    stdout=vcf_file, stderr=log)


    subprocess.call(["samtools", "view", "-q", "60", "-b", file_name + ".fixmate.100.bam"],
                    stdout=open(file_name + ".fixmate.100.q60.bam", "w"))


    subprocess.call(["samtools", "sort", file_name + ".fixmate.100.q60.bam",
                    "-o", file_name + ".fixmate.100.q60.ref.bam", "--reference", reference_path])


    subprocess.call(["samtools", "index", file_name + ".fixmate.100.q60.ref.bam"])


    subprocess.call(["bamtools", "index", "-in", file_name + ".fixmate.100.q60.ref.bam"])


    subprocess.call(["freebayes", "-p", "1", "-f", reference_path,
                    file_name + ".fixmate.100.q60.ref.bam"],
                    stdout=open(file_name + ".fixmate.100.q60.ref.vcf", "w"))


    with open(log_file, "a") as log:
         subprocess.call(["sh", "samtools_mpileup.sh", file_name], stdout=log, stderr=log)

    logging.info("Processing complete for file: %s", file_path)


pool = Pool()
pool.map(process_file, file_paths)
pool.close()
pool.join()


python_script = '''
import os

for file_num in range(1, 1000):
    file_name = 'file{}.fasta'.format(file_num)

    try:
        with open(file_name, 'r') as file:
            content = file.read()
            symbol_index = content.find('+')
            if symbol_index != -1:
                content = content[:symbol_index]

        # Get the name of the input FASTA file without the extension
        file_base_name = os.path.splitext(file_name)[0]

        # Rename the first line to the name of the input FASTA file
        content = content.replace("@reference", ">{}".format(file_base_name))

        # Print the modified content to the console
        print(content)

        # Create a new file with the '_assembly.fasta' suffix and write the modified content to it
        new_file_name = 'file{}_assembly.fasta'.format(file_num)
        with open(new_file_name, 'w') as new_file:
            new_file.write(content)

    except Exception as e:
        # Break the loop if an exception occurs (e.g., file doesn't exist)
        break

print("Processing complete.")
'''


with open("process_fasta.py", "w") as python_script_file:
    python_script_file.write(python_script)


subprocess.call(["python", "process_fasta.py"])


results_folder = "Assembly_Results"
if not os.path.exists(results_folder):
    os.makedirs(results_folder)


for file_path in glob.glob("*.sam") + glob.glob("*.bam") + glob.glob("*.vcf") + glob.glob("*.assembly.fasta") + glob.glob("*.bai"):
    os.rename(file_path, os.path.join(results_folder, file_path))


for fasta_file in glob.glob("file*.fasta"):
    os.rename(fasta_file, os.path.join(results_folder, os.path.basename(fasta_file)))


index_files = glob.glob("reference.fa.*") + glob.glob("reference.fasta.*")
for index_file in index_files:
    os.rename(index_file, os.path.join(results_folder, os.path.basename(index_file)))


logging.info("All processing complete.")

