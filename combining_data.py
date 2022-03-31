"""Combine all datasets into one."""
import pandas as pd

df = pd.concat(
    map(
        pd.read_csv,
        [
            "data/rideshare2018_reduced.csv",
            "data/rideshare_JanFebMar_reduced.csv",
            "data/rideshare_AprMayJun.csv",
            "data/jul_to_aug.csv",
            "data/2019oct_to_2020jan.csv",
        ],
    ),
    ignore_index=True,
)
df.to_csv("data/final_data.csv")
