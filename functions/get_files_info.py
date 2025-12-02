import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    
    if os.path.abspath(working_directory) not in os.path.abspath(full_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory\n' 
    
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory\n'
    
    contents = os.listdir(full_path)

    results = ""

    try:
        for file in contents:
            file_path = os.path.join(full_path, file)
            results = results + f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}\n"
        
        return results
    except Exception as e:
        return f"Error listing files: {e}"