"""Extract weather data for Chicago."""

import pandas as pd
import time
import requests
import json
import numpy as np
from datetime import datetime

# Access token
Token = "VSKeYyTUCtoWpuWvDhJswcCGPdgxbrma"

# Chicago weather station id
station_id = "GHCND:USW00014819"


def get_weather(station_id, bottom, top):
    """Get weather for a station."""
    # initialize lists to store data
    # make the api call
    r = requests.get(
        f"https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&dataypeid=TAVG&limit=1000&stationid={station_id}&startdate="
        + bottom
        + "&enddate="
        + top,
        headers={"token": Token},
        timeout=60,
    )
    # load the api response as a json
    d = json.loads(r.text)
    data = pd.DataFrame.from_dict(d["results"])
    time.sleep(1)
    return data


# separate by 2 month increments to reduce timeout chances
month_cuts = [
    ("-01-01", "-02-28"),
    ("-03-01", "-04-30"),
    ("-05-01", "-06-30"),
    ("-07-01", "-08-31"),
    ("-09-01", "-10-31"),
    ("-11-01", "-12-31"),
]


def get_segment(value, begin, end):
    """Get a segment of the data."""
    dfs = []
    # Iterate over years
    for year in range(begin, end):
        print(f"Starting year {year}")
        year_list = []
        # Iterate over month segments
        for tuple in month_cuts:
            print(f"starting tuple beginning in month {tuple[0][1:3]}")
            beginning = str(year) + tuple[0]
            end = str(year) + tuple[1]
            d = get_weather(value, beginning, end)
            year_list.append(d)
            pass
        year_df = pd.concat(year_list)
        # return list of year dataframes
        dfs.append(year_df)
    return dfs


if __name__ == "__main__":
    chicago = get_segment(station_id, 2018, 2021)
    # Concatenate dataframes
    chicago = pd.concat(chicago).reset_index(drop=True)
    # Keep only statistics of interest
    chicago = chicago[
        chicago["datatype"].isin(
            [
                "PRCP",
                "TMAX",
                "TMIN",
                "SNOW",
                "SNWD",
                "WSF2",
            ]
        )
    ]
    chicago["date_new"] = pd.DatetimeIndex(chicago["date"])
    chicago = chicago.fillna(0)
    # Turn data into tidy format
    temp = chicago.pivot_table(
        values="value",
        index=["date"],
        columns=["datatype"],
    ).reset_index()
    # Convert to imperial measurements
    temp["precip"] = temp["PRCP"] / (25.4)
    temp["snow"] = temp["SNOW"] / (25.4)
    temp["snow_depth"] = temp["SNWD"] / (25.4)
    temp["max_temp"] = ((temp["TMAX"] / 10) * 9 / 5) + 32
    temp["min_temp"] = ((temp["TMAX"] / 10) * 9 / 5) + 32
    temp["wind_speed"] = temp["WSF2"] * 2.23694
    # Keep new columns
    temp = temp[
        [
            "date",
            "max_temp",
            "min_temp",
            "precip",
            "snow",
            "snow_depth",
            "wind_speed",
        ]
    ]
    temp.to_csv("../10_original_data/weather.csv")
