import subprocess
import os
import glob

def run_command(command, description):
    """Run a command and print the result with a separator."""
    print(f"Running {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    
    if result.returncode != 0:
        print(f"Error running {description}: {result.stderr}\n")
        return False
    else:
        print("*********************************************************")
        print(f"{description} finished successfully.\n")
        print("*********************************************************")
        return True

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    tasks = [
        os.path.join(script_dir, "FastQC_analysis.py"),
        os.path.join(script_dir, "Quality_per_Read.py"),
        os.path.join(script_dir, "multi_png.py"),
        os.path.join(script_dir, "Trim_Adapters.py"),
        os.path.join(script_dir, "Pipeline_virus_assembly.py"),
        os.path.join(script_dir, "process_fasta.py"),
    ]
    
    task_descriptions = [os.path.basename(task) for task in tasks]
    
    assembly_files = glob.glob(os.path.join(script_dir, 'Assembly_Results', 'file*_assembly.fasta'))
    
    for task, description in zip(tasks, task_descriptions):
        if task.endswith(".py"):
            command = f"python {task}"
        else:
            command = task
        
        if not run_command(command, description):
            break
    
    for assembly_file in assembly_files:
        output_dir = os.path.join(script_dir, 'Annotation_Results', os.path.basename(assembly_file).replace('_assembly.fasta', ''))
        prokka_command = f"prokka --kingdom Viruses --outdir {output_dir} --prefix SARS-CoV-2 {assembly_file}"
        description = f"Prokka on {os.path.basename(assembly_file)}"
        
        if not run_command(prokka_command, description):
            break

if __name__ == "__main__":
    main()














