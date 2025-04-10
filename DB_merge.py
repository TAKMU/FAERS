import polars as pl
import glob
import re
import os
import json
import multiprocessing as mp

num_processes = 8

with open("dtype_FAERS_pl.json", "r") as f:
    raw_dtypes = json.load(f)


dtypes = {
    file_type: {col: getattr(pl, dtype) for col, dtype in schema.items()}
    for file_type, schema in raw_dtypes.items()
}


def read_txt_polars(file, file_type):
    try:
        df = pl.read_csv(
            file,
            separator="$",
            encoding="utf8-lossy",
            schema=dtypes.get(file_type, None),
            ignore_errors=True,
            truncate_ragged_lines = True
        )
        return df
    except Exception as e:
        print(f"Error reading {file}: {e}")
        return None

if __name__ == "__main__":
    all_files = glob.glob("data/*.txt")
    file_types = ["DEMO", "DRUG", "INDI", "OUTC", "REAC", "RPSR", "THER"]

    for file_type in file_types:
        pattern = re.compile(rf"{file_type}(\d+)q(\d+)", re.IGNORECASE)
        files = [f for f in all_files if pattern.search(os.path.basename(f))]

        with mp.Pool(processes=num_processes) as pool:
            dfs = pool.starmap(read_txt_polars, [(file, file_type) for file in files])

        dfs = [df for df in dfs if df is not None]

        if dfs:
            df_all = pl.concat(dfs)
            output_file = f"data/{file_type}_new.csv"
            df_all.write_csv(output_file)
            print(f"Saved {file_type} data to {output_file}")
        else:
            print(f"No valid files found for {file_type}")

    for file_path in all_files:
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
