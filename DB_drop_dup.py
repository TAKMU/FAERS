import polars as pl
import json
import multiprocessing as mp

num_processes = 8
# Load data types (Polars expects Python types like str, int, float)
with open("dtype_FAERS_pl.json", "r") as f:
    raw_dtypes = json.load(f)

# Convert to Polars dtypes
dtypes = {
    file_type: {col: getattr(pl, dtype) for col, dtype in schema.items()}
    for file_type, schema in raw_dtypes.items()
}

if __name__ == '__main__':
    demo_file = "data/DEMO_new.csv"
    df = pl.read_csv(
            demo_file,
            encoding="utf8-lossy",
            schema=dtypes["DEMO"],
            ignore_errors=True,
            truncate_ragged_lines = True
        )
    df =df.unique(subset=["primaryid"], keep="last")
    df.write_csv(demo_file)
      
