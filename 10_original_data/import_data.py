"""Load data from Socrata API."""

# Import packages
from site import check_enableusersite
from sodapy import Socrata
import pandas as pd
import numpy as np
from datetime import datetime

# Set up API
token = "dL93bWcHXE99lzC2Tyj7mJ4qR"
client = Socrata("data.cityofchicago.org", token, timeout=1000000)

# Where filter conditions for each month
where2019jan = "trip_start_timestamp>='2019-01-01T00:00:00.000' AND trip_start_timestamp<'2019-02-01T00:00:00.000' AND pickup_community_area IS NOT NULL AND dropoff_community_area IS NOT NULL"
where2019feb = "trip_start_timestamp>='2019-02-01T00:00:00.000' AND trip_start_timestamp<'2019-03-01T00:00:00.000' AND pickup_community_area IS NOT NULL AND dropoff_community_area IS NOT NULL"
where2019mar = "trip_start_timestamp>='2019-03-01T00:00:00.000' AND trip_start_timestamp<'2019-04-01T00:00:00.000' AND pickup_community_area IS NOT NULL AND dropoff_community_area IS NOT NULL"
where2019apr = "trip_start_timestamp>='2019-04-01T00:00:00.000' AND trip_start_timestamp<'2019-05-01T00:00:00.000' AND pickup_community_area IS NOT NULL AND dropoff_community_area IS NOT NULL"
where2019may = "trip_start_timestamp>='2019-05-01T00:00:00.000' AND trip_start_timestamp<'2019-06-01T00:00:00.000' AND pickup_community_area IS NOT NULL AND dropoff_community_area IS NOT NULL"
where2019jun = "trip_start_timestamp>='2019-06-01T00:00:00.000' AND trip_start_timestamp<'2019-07-01T00:00:00.000' AND pickup_community_area IS NOT NULL AND dropoff_community_area IS NOT NULL"
where2019jul = "trip_start_timestamp>='2019-07-01T00:00:00.000' AND trip_start_timestamp<'2019-08-01T00:00:00.000' AND pickup_community_area IS NOT NULL AND dropoff_community_area IS NOT NULL"
where2019aug = "trip_start_timestamp>='2019-08-01T00:00:00.000' AND trip_start_timestamp<'2019-09-01T00:00:00.000' AND pickup_community_area IS NOT NULL AND dropoff_community_area IS NOT NULL"
where2019sep = "trip_start_timestamp>='2019-09-01T00:00:00.000' AND trip_start_timestamp<'2019-10-01T00:00:00.000' AND pickup_community_area IS NOT NULL AND dropoff_community_area IS NOT NULL"
where2019oct = "trip_start_timestamp>='2019-10-01T00:00:00.000' AND trip_start_timestamp<'2019-11-01T00:00:00.000' AND pickup_community_area IS NOT NULL AND dropoff_community_area IS NOT NULL"
where2019nov = "trip_start_timestamp>='2019-11-01T00:00:00.000' AND trip_start_timestamp<'2019-12-01T00:00:00.000' AND pickup_community_area IS NOT NULL AND dropoff_community_area IS NOT NULL"
where2019dec = "trip_start_timestamp>='2019-12-01T00:00:00.000' AND trip_start_timestamp<'2020-01-01T00:00:00.000' AND pickup_community_area IS NOT NULL AND dropoff_community_area IS NOT NULL"
where2020jan = "trip_start_timestamp>='2020-01-01T00:00:00.000' AND trip_start_timestamp<'2020-02-01T00:00:00.000' AND pickup_community_area IS NOT NULL AND dropoff_community_area IS NOT NULL"

# Added to a list for convenience (Not needed if not running function in loop)
year2019_count = [
    where2019jan,
    where2019feb,
    where2019mar,
    where2019apr,
    where2019may,
    where2019jun,
    where2019jul,
    where2019aug,
    where2019sep,
    where2019oct,
    where2019nov,
    where2019dec,
    where2020jan,
]

# List of counts for each month (Not needed if not running function in loop)
counts_bymonth = []
for month in year2019_count:
    count = client.get(
        "m6dm-c72p",
        select="COUNT(*)",
        where=month,
    )
    counts_bymonth.append(count)


def get_count(where_filter):
    """Count function. Returns in format of '[{'COUNT': 'XXXXXXX'}]'"""
    count = client.get(
        "m6dm-c72p",
        select="COUNT(*)",
        where=where_filter,
    )
    return count


def paging_data(where_filter, count):
    """Paging data with 1,000,000 per chunk.

    Play around with the chunk_size if 1 million is too large (roughly 500,000 - 1mil would be ideal).
    where_filter: filter condition (string).
    count: output from get_count function.

    Function returns a dataframe with selected month.
    """
    start = 0
    chunk_size = 1000000
    results = []
    while True:
        results.extend(
            client.get(
                "m6dm-c72p",
                select="trip_start_timestamp,trip_end_timestamp,trip_seconds,trip_miles,pickup_community_area,dropoff_community_area,fare,tip,additional_charges,shared_trip_authorized,trips_pooled,pickup_centroid_location,dropoff_centroid_location",
                where=where_filter,
                offset=start,
                limit=chunk_size,
            )
        )
        start += chunk_size
        print("chunk: " + str(start))
        if start > int(count[0]["COUNT"]):
            break
    df = pd.DataFrame.from_records(results)
    return df


def reduce_data(df):
    """Takes output dataframe from paging_data and select 0.1% of data from every day.

    Returns a dataframe which can then be concatinated with other dataframes and returned
    as .csv.
    """
    np.random.seed(1234)
    df["trip_start_timestamp"] = pd.to_datetime(df["trip_start_timestamp"])
    df["date"] = pd.to_datetime(df["trip_start_timestamp"]).dt.strftime("%Y-%m-%d")
    df_reduced = df.groupby("date").sample(frac=0.001)
    return df_reduced


if __name__ == "__main__":
    # Example of how to get a dataframe for January 2019
    df2019jan = paging_data(where2019jan, get_count(where2019jan))
    df2019jan_reduced = reduce_data(df2019jan)
    df2019jan_reduced.to_csv("path")