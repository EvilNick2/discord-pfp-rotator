import os
import json



if os.path.exists('config.json'):
		with open('config.json', 'r') as file:
				config = json.load(file)

def rename_files_in_folder(folder_path, new_name_base, start_number=1):
	files = os.listdir(folder_path)

	files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

	files.sort()

	number = start_number

	for file in files:
		new_name = f"{new_name_base}{number}.jpg"
		old_file = os.path.join(folder_path, file)
		new_file = os.path.join(folder_path, new_name)

		os.rename(old_file, new_file)

		number += 1

folder_path = config["avatars_dir"]
rename_files_in_folder(folder_path, 'avatar_', start_number=1)