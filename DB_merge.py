import pandas as pd
import fnmatch
import re
import os

all_files = os.listdir("data/")
file_types = ["DEMO", "DRUG", "INDI", "OUTC", "REAC", "RPSR", "THER"]    
for file_type in file_types:
    df_ls = []
    pattern = re.compile(rf"{file_type}(\d+)q(\d+)", re.IGNORECASE)
    files = [f for f in all_files if pattern.search(f)]
    for file in files:
        match = re.search(rf"{file_type}(\d+)[qQ](\d+)", file, flags=re.IGNORECASE)
        if match:
            year, quarter = int(match.group(1)), int(match.group(2))
        if year < 14 or (year == 14 and quarter < 3):
            os.remove(f"data/{file}")
            continue
        file_name = f"data/{file}"
        df = pd.read_csv(f"data/{file}", low_memory=False, index_col="primaryid", on_bad_lines='skip', encoding_errors='ignore')
        os.remove(f"data/{file}")
        df_ls.append(df)
    df_all = pd.concat(df_ls)
    df_all.to_csv(f"data/{file_type}.csv")
    
