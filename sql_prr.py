import numpy as np
import re
import os

import psycopg2
from sshtunnel import SSHTunnelForwarder
import pandas as pd
import concurrent.futures as futures
import dask.dataframe as dd
import glob
from dotenv import load_dotenv

load_dotenv() 
SSH_USER = os.environ.get("SSH_USER")
SSH_ADDRESS = os.environ.get("SSH_ADDRESS")
SSH_PSSWD = os.environ.get("SSH_PSSWD")
SSH_PORT = int(os.environ.get("SSH_PORT_REMOTE"))

DB_IP = os.environ.get("DB_IP")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PSSWD = os.environ.get("DB_PSSWD")

def reac_data(drug):
   print(f"Starting {drug}")
   
   cursor = connection.cursor()
   query = f"""SELECT pt, prod_ai, count(primaryid) AS no_reactions FROM DRUG 
               INNER JOIN REAC USING(primaryid)
               WHERE prod_ai ILIKE '{drug}%' 
               GROUP BY pt, prod_ai
               """
   cursor.execute(query)
   data = cursor.fetchall()
   if len(data) > 0: 
      column_names = [desc[0] for desc in cursor.description]
      df = pd.DataFrame(data, columns=column_names)
      df["prod_ai"] = drug
      df = df.groupby(["pt", "prod_ai"])["no_reactions"].sum().reset_index()
      file_path = f"./drugs/{drug}/adr_real.csv"
      df.to_csv(file_path, index=False)
   cursor.close()
   
   return f"Finish {drug}"




try:

    with SSHTunnelForwarder(
         (SSH_ADDRESS, SSH_PORT),
         ssh_username=SSH_USER,
         ssh_password=SSH_PSSWD, 
         remote_bind_address=("localhost", 5432)) as server:
         
         server.start()
         print ("server connected")
         connection = psycopg2.connect(
                        host=DB_IP,
                        database=DB_NAME,
                        user=DB_USER,
                        password=DB_PSSWD,
                        port=server.local_bind_port
                     )
         cursor = connection.cursor()
         query = f"""SELECT pt, count(*) AS no_events_global FROM REAC 
               GROUP BY pt
               """
         cursor.execute(query)
         data_global = cursor.fetchall()
         if len(data_global) > 0: 
            column_names = [desc[0] for desc in cursor.description]
            df_global = pd.DataFrame(data_global, columns=column_names)
            file_path = f"./data/adr_global.csv"
            df_global.to_csv(file_path, index=False)
            total_reactions_global= df_global["no_events_global"].sum()
            print(total_reactions_global)
         if __name__ == '__main__':
            pattern = "./drugs/*/adr_real.csv"  
            files_to_delete = glob.glob(pattern)
            for file_path in files_to_delete:
                try:
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")
            study = pd.read_csv("./Antidepressives.csv", low_memory=False, on_bad_lines='skip', encoding_errors='ignore')
            drugs = study["Drug"].to_list()

            with futures.ThreadPoolExecutor() as e:
               f = [e.submit(reac_data, drug) for drug in drugs]
               for r in futures.as_completed(f):
                  print(r.result())
            
            pattern = "./drugs/*/adr_real.csv"  
            df = dd.read_csv(pattern)
            df['no_reactions'].astype(int)
            total_reactions_antidep = df["no_reactions"].sum().compute()

            # Perform groupby and sum aggregation
            result = df.groupby(['pt'])["no_reactions"].sum().reset_index().compute()
            result = result.rename(columns={'no_reactions': 'total_pt'})
            #New line (to check Proportional Reporting Ratio)
            df_final = df.merge(result, on="pt", how="inner")
            result = df.groupby(['prod_ai'])["no_reactions"].sum().reset_index().compute()
            result = result.rename(columns={'no_reactions': 'total_events_drug'})
            df_final = df_final.merge(result, on="prod_ai", how="inner")
            df_final = df_final.merge(df_global, on="pt", how="inner")
            print(df_final.head())

            # Write result to a CSV file
            df_final.to_csv("./drugs/adr_summary_real.csv", index=False) 
            df_final["prr_global"] = (df_final["no_reactions"]/df_final["total_events_drug"])/((df_final["no_events_global"] - df_final["no_reactions"])/(total_reactions_global- df_final["total_events_drug"]))
            df_final["prr_local"] = (df_final["no_reactions"]/df_final["total_events_drug"])/((df_final["total_pt"]- df_final["no_reactions"])/(total_reactions_antidep - df_final["total_events_drug"]))
            df_filtered = df_final.query("no_events_global < total_pt ")
            print(df_filtered.head())
            df_filtered.to_csv("errors.csv", index=False)
            df_final.to_csv("prr_real_test.csv", index=False)
            connection.close()
except Exception as error:
    print ("Connection Failed")
    print(error)

