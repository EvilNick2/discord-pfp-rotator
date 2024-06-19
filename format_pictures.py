import os
from main import load_config

config = load_config()

def rename_files_in_folder(folder_path, new_name_base, start_number=1):
	# List all files in the folder
	files = os.listdir(folder_path)
	# Optional: Filter out directories, keep files only
	files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
	# Sort files if needed
	files.sort()
	# Initialize the starting number
	number = start_number
	# Loop through each file and rename it
	for file in files:
		# Define the new file name
		new_name = f"{new_name_base}{number}.jpg"  # Assuming the files are .jpg, change as needed
		# Define the full path for the old and new names
		old_file = os.path.join(folder_path, file)
		new_file = os.path.join(folder_path, new_name)
		# Rename the file
		os.rename(old_file, new_file)
		# Increment the number for the next file
		number += 1

# Example usage
folder_path = config["avatars_dir"]
rename_files_in_folder(folder_path, 'avatar_', start_number=1)