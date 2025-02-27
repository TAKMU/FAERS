import pandas as pd
import os

if __name__ == '__main__':
    demo_file = "data/DEMO.csv"
    df = pd.read_csv(demo_file, low_memory=False, index_col="primaryid", on_bad_lines='skip', encoding_errors="ignore", dtype={"primaryid": "string"})
    df = df.reset_index()
    df = df.drop_duplicates(subset=["primaryid"])
    df.to_csv(demo_file, na_rep='NULL', index=False)
      
