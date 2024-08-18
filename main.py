import subprocess
import os


script_dir = os.path.dirname(os.path.abspath(__file__))


tasks = [
    os.path.join(script_dir, "FastQC_analysis.py"),
    os.path.join(script_dir, "Quality_per_read.py"),
    os.path.join(script_dir, "multi_png.py"),
    os.path.join(script_dir, "Trim_Adapters.py"),
    os.path.join(script_dir, "Pipeline_virus_assembly.py"),
    os.path.join(script_dir, "process_fasta.py"),
    f"prokka --kingdom Viruses --outdir {os.path.join(script_dir, 'Annotation_Results')} --prefix SARS-CoV-2 {os.path.join(script_dir, 'Assembly_Results', 'file1_assembly.fasta')}",
]

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
        print(f"{task} The genome assembly and annotation has finished successfully.\n")

