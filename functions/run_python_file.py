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
    try:
        completed_process = subprocess.run(args, capture_output=True, cwd=abs_working_dir, timeout=30)
        return f'STDOUT: {completed_process.stdout} STDERR: {completed_process.stderr}'
    except Exception as e:
        return f'Error: Executing Python file: {e}'
