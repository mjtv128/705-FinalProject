"""Clean final data."""

import pandas as pd
import geopandas as gpd
import calendar
import numpy as np


def clean_data(path: str) -> pd.DataFrame:
    """Read in data and remove nulls and outliers."""
    df = pd.read_csv(path)
    # Convert timestamps to datetime objects
    df["trip_end_timestamp"] = pd.to_datetime(df["trip_end_timestamp"])
    df["trip_start_timestamp"] = pd.to_datetime(df["trip_start_timestamp"])
    # Drop mismatched index columns and unneeded longitude
    df = df.drop(
        [
            "Unnamed: 0",
            "pickup_centroid_location",
            "dropoff_centroid_location",
        ],
        axis=1,
    )
    # Remove rows with missing data
    df = df.dropna()
    # Remove time outlier
    df = df[df["trip_seconds"] < 70000]
    return df


def community_names(df: pd.DataFrame, path: str) -> pd.DataFrame:
    """Get Community Area names for pickup and dropoff."""
    # Read in community data
    ca = pd.DataFrame(gpd.read_file(path)).drop(["geometry"], axis=1)
    # Create duplicate community data for merging
    ca = ca[["community", "area_numbe"]]
    ca["area_numbe"] = ca["area_numbe"].astype(int)
    pickup_ca = ca.rename(
        columns={
            "area_numbe": "pickup_community_area",
            "community": "pickup_community_name",
        }
    )
    dropoff_ca = ca.rename(
        columns={
            "area_numbe": "dropoff_community_area",
            "community": "dropoff_community_name",
        }
    )
    # Merge to get names of community area for pickup and dropoff
    merge_temp = pd.merge(
        df, pickup_ca, on="pickup_community_area", validate="m:1"
    ).drop(["pickup_community_area"], axis=1)
    # Create final dataframe
    final_df = pd.merge(
        merge_temp, dropoff_ca, on="dropoff_community_area", validate="m:1"
    ).drop(["dropoff_community_area"], axis=1)
    return final_df


def new_variables(df: pd.DataFrame) -> pd.DataFrame:
    """Create new variables."""
    df["year"] = df["trip_start_timestamp"].dt.year
    df["month"] = df["trip_start_timestamp"].dt.month.apply(
        lambda x: calendar.month_name[x]
    )
    df["day"] = df["trip_start_timestamp"].dt.day
    df["day_of_week"] = df["trip_start_timestamp"].dt.dayofweek
    df["hour"] = df["trip_start_timestamp"].dt.hour
    df["weekend"] = np.where(df["day_of_week"] >= 4, 1, 0)
    df["day_of_week"] = df["day_of_week"].apply(lambda x: calendar.day_name[x])
    df["nonzero_tip"] = np.where(df["tip"] > 0, 1, 0)
    return df


def split_export(df: pd.DataFrame) -> None:
    """Split data and export to csv."""
    np.random.seed(3320)
    train, validate, test = np.split(
        df.sample(frac=1),
        [
            int(0.7 * len(df)),
            int(0.8 * len(df)),
        ],
    )
    train.to_csv("../15_modified_data/train_data.csv", index=False)
    validate.to_csv("../15_modified_data/val_data.csv", index=False)
    test.to_csv("../15_modified_data/test_data.csv", index=False)
    pass


if __name__ == "__main__":
    df = clean_data("../15_modified_data/final_data.csv")
    print(df.columns)
    df = community_names(df, "../10_original_data/community_areas.geojson")
    df = new_variables(df)
    split_export(df)
