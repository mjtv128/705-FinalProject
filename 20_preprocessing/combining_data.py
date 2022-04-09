"""Combine all datasets into one."""
import pandas as pd

# Read in all uber data
df = pd.concat(
    map(
        pd.read_csv,
        [
            "../10_original_data/rideshare2018_reduced.csv",
            "../10_original_data/rideshare_JanFebMar_reduced.csv",
            "../10_original_data/rideshare_AprMayJun.csv",
            "../10_original_data/jul_to_aug.csv",
            "../10_original_data/2019oct_to_2020jan.csv",
        ],
    ),
    ignore_index=True,
)

# Read in weather data
weather = pd.read_csv("../10_original_data/weather.csv")
weather["date"] = pd.DatetimeIndex(weather["date"])
weather["merge"] = weather["date"].dt.strftime("%Y/%m/%d")
df["trip_start_timestamp"] = pd.DatetimeIndex(df["trip_start_timestamp"])
df["merge"] = df["trip_start_timestamp"].dt.strftime("%Y/%m/%d")
weather = weather.fillna(0)

# Merge weather data
new = pd.merge(df, weather, how="left", on="merge")
new = new.drop(
    [
        "Unnamed: 0_x",
        "Unnamed: 0.1",
        "Unnamed: 0_y",
        "merge",
        "date_y",
    ], axis = 1
)
new = new.rename(columns = {"date_x":"date"})

new.to_csv("15_modified_data/final_data.csv")
