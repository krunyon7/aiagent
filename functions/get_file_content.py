import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads file truncated to at most {MAX_CHARS} characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read the file from, relative to the working directory. If not provided, returns an error.",
            ),
        },
        required=["file_path"]
    ),
)

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_file_path, "r") as f:
            
            trunc_msg = ""
            file_content_string = f.read(MAX_CHARS)
            if len(f.read()) > MAX_CHARS:
                trunc_msg = f'[...File "{file_path}" truncated at 10000 characters]'
        return file_content_string + trunc_msg
    except Exception as e:
        return f"Error reading file: {e}"

