import subprocess
import os

def trim_adapters(input_dir, output_dir, adapter_list_file):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(adapter_list_file, 'r') as file:
        adapter_sequences = [line.strip() for line in file if line.strip()]

    fastq_files = [f for f in os.listdir(input_dir) if f.endswith(".fastq")]

    for file in fastq_files:
        input_file = os.path.join(input_dir, file)
        base_filename = file.replace(".fastq", "")
        current_input_file = input_file

        for adapter_sequence in adapter_sequences:

            temp_output_file = os.path.join(output_dir, f"{base_filename}_temp.fastq")

            command = [
                "cutadapt",
                "-a", adapter_sequence,        # Adapter sequence to trim
                "-o", temp_output_file,        # Temporary output file
                current_input_file             # Current input file
            ]


            try:
                subprocess.run(command, check=True, text=True, capture_output=True)
                print(f"Trimmed {file} with adapter {adapter_sequence} and saved to {temp_output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error during trimming with adapter {adapter_sequence} for {file}: {e.stderr}")

            current_input_file = temp_output_file

        final_output_file = os.path.join(output_dir, f"{base_filename}.fastq")
        os.rename(temp_output_file, final_output_file)
        print(f"Final trimmed file for {file} is saved to {final_output_file}")

        if os.path.exists(temp_output_file):
            os.remove(temp_output_file)
            print(f"Deleted temporary file {temp_output_file}")

if __name__ == "__main__":
    # Define the input directory, output directory, and adapter list file
    input_directory = "RAW_DATA"         # Directory containing input FASTQ files
    output_directory = "TRIMMED_DATA"    # Directory to save trimmed FASTQ files
    adapter_list_file = "RAW_DATA/Adapter_List.txt"  # File containing adapter sequences
    
    trim_adapters(input_directory, output_directory, adapter_list_file)


