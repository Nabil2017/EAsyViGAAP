import subprocess
import os
import glob

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# List of tasks to run (Python scripts and command-line)
tasks = [
    os.path.join(script_dir, "FastQC_analysis.py"),
    os.path.join(script_dir, "Quality_per_read.py"),
    os.path.join(script_dir, "multi_png.py"),
    os.path.join(script_dir, "Trim_Adapters.py"),
    os.path.join(script_dir, "Pipeline_virus_assembly.py"),
    os.path.join(script_dir, "process_fasta.py"),
]

# Find all files matching the pattern "file*_assembly.fasta"
assembly_files = glob.glob(os.path.join(script_dir, 'Assembly_Results', 'file*_assembly.fasta'))

# Run each task
for task in tasks:
    if task.endswith(".py"):
        command = f"python {task}"
    else:
        command = task
    
    print(f"Running {task}...")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    print(result.stdout)
    
    if result.returncode != 0:
        print(f"Error running {task}: {result.stderr}\n")
        break  
    else:
        print(f"{task} finished successfully.\n")

# Run Prokka for each assembly file
for assembly_file in assembly_files:
    prokka_command = f"prokka --kingdom Viruses --outdir {os.path.join(script_dir, 'Annotation_Results')} --prefix SARS-CoV-2 {assembly_file}"
    print(f"Running Prokka on {assembly_file}...")
    
    result = subprocess.run(prokka_command, shell=True, capture_output=True, text=True)
    
    print(result.stdout)
    
    if result.returncode != 0:
        print(f"Error running Prokka on {assembly_file}: {result.stderr}\n")
        break  
    else:
        print(f"Prokka finished successfully for {assembly_file}.\n")

