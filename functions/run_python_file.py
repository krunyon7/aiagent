import os, subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs Python file in specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to run the Python file from, relative to the working directory. If not provided, returns an error.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file."
                ),
                description="Optional arguments to pass to the Python file."
            )
        },
        required=["file_path"]
    ),
)

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
