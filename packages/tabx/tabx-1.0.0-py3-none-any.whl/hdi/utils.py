import os

def validate_file_path(file_path):
    """Check if the provided file path exists and is a valid file."""
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return True
    else:
        print(f"[Error] Invalid file path: {file_path}")
        return False

def create_output_directory(output_path):
    """Create output directory if it doesn't exist."""
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"[Info] Created output directory at {output_path}")
    else:
        print(f"[Info] Output directory already exists at {output_path}")
