import os, subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_file_path):
        return f'Error: File "{file_path}" not found.'
    if not target_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    sub_args = ["python3", target_file_path] + args
    try:
        completed_process = subprocess.run(
            sub_args, 
            capture_output=True,
            text=True, 
            cwd=abs_working_dir, 
            timeout=30,
            check=True
        )
        result = []
        if completed_process.stdout:
            result.append(f"STDOUT:\n {completed_process.stdout}") 
        if completed_process.stderr:
            result.append(f"STDERR: {completed_process.stderr}")
        if completed_process.returncode != 0:
            result.append(f"Process exited with code {completed_process.returncode}")
        return "\n".join(result) if result else "No output produced."
    except Exception as e:
        return f'Error: Executing Python file: {e}'
