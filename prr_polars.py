import polars as pl
import concurrent.futures as futures


study = pl.read_csv("./Drugs.csv")

study = study.select(
    pl.col("Drug").str.to_lowercase()
)


df_drug = pl.read_csv("data/DRUG.csv", columns=["primaryid", "prod_ai"])
df_drug = df_drug.select(
    pl.col("primaryid"),
    pl.col("prod_ai").str.to_lowercase()
)

df_reac = pl.read_csv("data/REAC.csv", columns=["primaryid", "pt"])


def filter_drug(drug):
    global df_drug
    global df_reac

    result = df_drug.filter(
       pl.col("prod_ai").str.contains(rf"([^a-zA-Z]){drug}")|
       pl.col("prod_ai").str.starts_with(drug)
    )
    result = result.join(df_reac, on="primaryid", how="inner")
    result = result.select(
        pl.lit(drug).alias("prod_ai"),
        pl.col("pt")
        )
    result = result.group_by(
        pl.col("pt"),
        pl.col("prod_ai")
    ).agg(
        pl.len().alias("len")
    )
    result = result.with_columns(
        #Total reactions per drug 
    pl.col("len").sum().alias("reactions_per_drug")
)
    return result



drugs = study["Drug"].to_list()
if __name__ == '__main__':
    dfs = []
    with futures.ThreadPoolExecutor() as e:
       f = [e.submit(filter_drug, drug) for drug in drugs]
       for r in futures.as_completed(f):
          dfs.append(r.result())
    df_group = pl.concat(dfs)
    df_group = df_group.with_columns(
        pl.col("pt").count().over("pt").alias("pt_total_local")
        )
    total_reactions_local = df_group.select(pl.col("pt_total_local").sum()).item()
    df_reac_global = df_reac.group_by(
        pl.col("pt")
    ).agg(
        pl.len().alias("pt_total_global")
    )
    total_reactions_global = df_reac_global.select(pl.col("pt_total_global").sum()).item()

    df_group = df_group.join(df_reac_global, on="pt", how="left")
    df_final = df_group.with_columns(
        (
            (pl.col("len")/pl.col("reactions_per_drug"))/
            ((pl.col("pt_total_global")-pl.col("len"))/(total_reactions_global-pl.col("reactions_per_drug")))            
        ).alias("prr_global"),
        (
            (pl.col("len")/pl.col("reactions_per_drug"))/
            ((pl.col("pt_total_local")-pl.col("len"))/(total_reactions_local-pl.col("reactions_per_drug")))
        ).alias("prr_local")
   )
    df_prr = df_final.select(
        pl.col("prod_ai"),
        pl.col("pt"),
        pl.col("prr_local"),
        pl.col("prr_global")
    )

    df_filtered_local = df_prr.filter(
        (pl.col("prr_local") != float("inf"))
    ) 
    
    df_filtered_local = df_filtered_local.select(
        pl.col("prod_ai"),
        pl.col("pt"),
        pl.col("prr_local")
    )
    
    df_filtered_local.write_csv("data/prr_results_ad_local_ad.csv")


    df_filtered_global = df_prr.filter(
        (pl.col("prr_global") != float("inf")) 
    )
    
    df_filtered_global = df_filtered_global.select(
        pl.col("prod_ai"),
        pl.col("pt"),
        pl.col("prr_global")
    )

    df_filtered_global.write_csv("data/prr_results_ad_global_ad.csv")
    print(total_reactions_local)
    print(total_reactions_global)

    
   