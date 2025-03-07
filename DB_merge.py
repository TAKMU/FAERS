import pandas as pd
import re
import os
import json
import glob
import multiprocessing as mp

num_processes = 8

# Load data types from JSON
with open("dtype_FAERS.json", "r") as f:
    dtypes = json.load(f)

# Function to read a single text file and allow multiprocessing
def read_txt(file, file_type):
    try:
        df = pd.read_csv(
            file,  
            delimiter="$",
            low_memory=False,
            on_bad_lines="skip",
            encoding_errors="ignore",
            dtype=dtypes.get(file_type, None)  
        )
        return df
    except Exception as e:
        print(f"Error reading {file}: {e}")
        return None


if __name__ == "__main__": 
    all_files = glob.glob("data/*.txt")
    file_types = ["DEMO", "DRUG", "INDI", "OUTC", "REAC", "RPSR", "THER"]
    
    #Merge files according to file type
    for file_type in file_types:
        pattern = re.compile(rf"{file_type}(\d+)q(\d+)", re.IGNORECASE)
        
        files = [f for f in all_files if pattern.search(os.path.basename(f))]
    
        with mp.Pool(processes=num_processes) as pool:
            dfs = pool.starmap(read_txt, [(file, file_type) for file in files])
        dfs = [df for df in dfs if df is not None]
        df_all = pd.concat(dfs, ignore_index=True)
        
        output_file = f"data/{file_type}.csv"
        df_all.to_csv(output_file, index=False)
        print(f"Saved {file_type} data to {output_file}")
    
    #Delete .txt files
    for file_path in all_files:
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}") 