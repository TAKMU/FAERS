import zipfile
import os
import re
import glob
# Specify the directory containing the zip files
destination_dir = r"data"

# Iterate through years and extract files
pattern = r"data/faers_ascii_20" + r"[1-2][0-9]" + r"[qQ][1-4].zip"
files = glob.glob(pattern)
    # Find and extract files matching the pattern
print(files)
for filename in files:
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        members = zip_ref.infolist()
        filtered_members = [
            member for member in members if (member.filename.startswith('ASCII') or member.filename.startswith('ascii') ) and member.filename.endswith('.txt')
        ]
        for member in filtered_members:
            zip_ref.extract(member, "data/")
            extracted_path = os.path.join(destination_dir, member.filename)
            final_path = os.path.join(destination_dir, os.path.basename(member.filename))
            os.rename(extracted_path, final_path)
    os.remove(filename)

    print(f"Moved from {filename}")
