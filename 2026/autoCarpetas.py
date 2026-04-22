import os

# Path to the FONDOS directory relative to this script
fondos_path = os.path.join(os.path.dirname(__file__), '..', '..', 'AUDIOS')

# Get the directory where this script is located
current_dir = os.path.dirname(__file__)

# List all files in FONDOS
for file in os.listdir(fondos_path):
    file_path = os.path.join(fondos_path, file)
    if os.path.isfile(file_path):
        # Get the filename without extension
        name = os.path.splitext(file)[0]
        # Create the folder in the current directory
        folder_path = os.path.join(current_dir, name)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {name}")