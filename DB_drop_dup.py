import pandas as pd
import json

with open("dtype_FAERS.json", "r") as f:
    dtypes = json.load(f)

if __name__ == '__main__':
    demo_file = "data/DEMO.csv"
    df = pd.read_csv(demo_file, 
                     low_memory=False, 
                     on_bad_lines='skip', 
                     encoding_errors="ignore", 
                     dtype=dtypes["DEMO"])
    df = df.drop_duplicates(subset=["primaryid"])
    df.to_csv(demo_file, na_rep='NULL', index=False)
      
