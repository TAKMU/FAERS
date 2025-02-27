import pandas as pd
import os
import glob

data_dir = "data/"
pattern = "data/[A-Za-z][A-Za-z][A-Za-z][A-Za-z][0-9][0-9][qQ][1-4]*.txt"
files_ascii = glob.glob(pattern)
for file in files_ascii:
    base_name = os.path.basename(file)
    base_name_csv = base_name.replace(".txt", ".csv")
    csv_file = data_dir + base_name_csv
    df = pd.read_csv(file, delimiter="$", low_memory=False, index_col="primaryid", on_bad_lines='skip', encoding_errors='ignore')
    df.to_csv(csv_file)
    print(csv_file)
    os.remove(file)    
