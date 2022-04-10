"""Explore and visualize Uber data."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import contextily as cx

plt.rcParams["figure.figsize"] = (15, 10)
plt.rcParams.update({"font.size": 15})


def read_in(files: list[str]) -> pd.DataFrame:
    """Read in data all data for exploration."""
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    return df


def summary_stats(df: pd.DataFrame) -> None:
    """Summary statistics and histogram."""
    rows = df.shape[0]
    print(f"There are {rows} rides in the data.")
    tip_rows = (df["nonzero_tip"] == 1).sum()
    perc = round(100 * tip_rows / rows, 2)
    print(f"There are {tip_rows} rides that had a tip, or {perc}%.")
    nonzeros = df[df["nonzero_tip"] == 1]
    plt.hist(nonzeros["tip"], bins=30)
    plt.xlabel("Tip Value")
    plt.ylabel("Frequency")
    plt.title("Histogram of Tips (Excluding Non-Tip Rides)")
    plt.savefig("../26_images/hist.png")
    plt.show()


def graph_time(df: pd.DataFrame) -> None:
    """Graph proportion of tipped rides by time features."""
    # By Hour
    grouped_data = (
        df.groupby(["hour"])
        .agg(
            {"nonzero_tip": "sum"},
        )
        .reset_index()
    )
    grouped_data2 = (
        df.groupby(["hour"])
        .agg(
            {"nonzero_tip": "count"},
        )
        .reset_index()
    )
    final = pd.merge(grouped_data, grouped_data2, on=["hour"], how="inner")
    final["tipped_rides"] = final["nonzero_tip_x"] / final["nonzero_tip_y"]
    plt.bar(final["hour"], final["tipped_rides"])
    plt.ylim([0.10, 0.21])
    plt.title("Percentage of Rides Tipped by Hour Initiated")
    plt.xlabel("Hour")
    plt.ylabel("Proportion of Rides ending in Tip")
    plt.savefig("../26_images/tip_by_hour.png")
    plt.show()
    # By Day
    grouped_data = (
        df.groupby(["day_of_week"])
        .agg(
            {"nonzero_tip": "sum"},
        )
        .reset_index()
    )
    grouped_data2 = (
        df.groupby(["day_of_week"])
        .agg(
            {"nonzero_tip": "count"},
        )
        .reset_index()
    )
    final = pd.merge(
        grouped_data,
        grouped_data2,
        on=["day_of_week"],
        how="inner",
    )
    final["tipped_rides"] = final["nonzero_tip_x"] / final["nonzero_tip_y"]
    plt.bar(final["day_of_week"], final["tipped_rides"])
    plt.title("Percentage of Rides Tipped by Day of Week")
    plt.xlabel("Day of Week")
    plt.ylim([0.12, 0.195])
    plt.ylabel("Proportion of Rides ending in Tip")
    plt.tight_layout()
    plt.savefig("../26_images/tip_by_day.png")
    plt.show()


def numerical_boxplots(df: pd.DataFrame) -> None:
    """Boxplots for continuous variables."""
    # Trip Length
    sns.boxplot(y="trip_seconds", x="nonzero_tip", data=df, fliersize=0)
    plt.ylim([0, 3000])
    plt.xlabel("Nonzero Tip?")
    plt.ylabel("Trip Seconds")
    plt.title("Trip Length in Seconds by Tip Presence")
    plt.savefig("../26_images/tip_by_seconds.png")
    plt.show()
    # Trip Fare
    sns.boxplot(y="fare", x="nonzero_tip", data=df, fliersize=0)
    plt.ylim([0, 38])
    plt.xlabel("Nonzero Tip?")
    plt.title("Trip Fare by Tip Presence")
    plt.savefig("../26_images/tip_by_fare.png")
    plt.show()


def geographic_plots(df: pd.DataFrame, path: str) -> None:
    """Graph tips by Chicago area."""
    ca = gpd.read_file(path)
    ca = ca[["community", "geometry"]].rename(
        {"community": "pickup_community_name"}, axis=1
    )
    grouped_data = (
        df.groupby(["pickup_community_name"])
        .agg(
            {"nonzero_tip": "sum"},
        )
        .reset_index()
    )
    grouped_data2 = (
        df.groupby(["pickup_community_name"])
        .agg({"nonzero_tip": "count"})
        .reset_index()
    )
    final = pd.merge(
        grouped_data,
        grouped_data2,
        on=["pickup_community_name"],
        how="inner",
    )
    final["tipped_rides"] = final["nonzero_tip_x"] / final["nonzero_tip_y"]
    pickup = ca.merge(
        final,
        on="pickup_community_name",
        how="inner",
        validate="1:1",
    )
    csfont = {"fontname": "Arial"}
    ax = pickup.plot(
        figsize=(15, 15),
        column="tipped_rides",
        cmap="Reds",
        legend=True,
        legend_kwds={
            "shrink": 0.5,
            "label": "Proportion of Rides Ending in Tip",
        },
        alpha=0.8,
        edgecolor="#808080",
    )
    cx.add_basemap(ax, crs="EPSG:4326", source=cx.providers.CartoDB.Voyager)
    ax.set_axis_off()
    ax.set_title(f"Tip Rate by Pickup Area", fontsize=20, **csfont)
    plt.savefig("../26_images/tip_by_pickup_area.png")
    plt.show()
    ca = ca.rename({"pickup_community_name": "dropoff_community_name"}, axis=1)
    grouped_data = (
        df.groupby(["dropoff_community_name"])
        .agg(
            {"nonzero_tip": "sum"},
        )
        .reset_index()
    )
    grouped_data2 = (
        df.groupby(["dropoff_community_name"])
        .agg({"nonzero_tip": "count"})
        .reset_index()
    )
    final = pd.merge(
        grouped_data,
        grouped_data2,
        on=["dropoff_community_name"],
        how="inner",
    )
    final["tipped_rides"] = final["nonzero_tip_x"] / final["nonzero_tip_y"]
    dropoff = ca.merge(
        final,
        on="dropoff_community_name",
        how="inner",
        validate="1:1",
    )
    ax = dropoff.plot(
        figsize=(15, 15),
        column="tipped_rides",
        cmap="Reds",
        legend=True,
        legend_kwds={
            "shrink": 0.5,
            "label": "Proportion of Rides Ending in Tip",
        },
        alpha=0.8,
        edgecolor="#808080",
    )
    cx.add_basemap(ax, crs="EPSG:4326", source=cx.providers.CartoDB.Voyager)
    ax.set_axis_off()
    ax.set_title(f"Tip Rate by Dropoff Area", fontsize=20, **csfont)
    plt.savefig("../26_images/tip_by_dropoff_area.png")
    plt.show()
    pass


if __name__ == "__main__":
    df = read_in(
        [
            "../15_modified_data/test_data.csv",
            "../15_modified_data/train_data.csv",
            "../15_modified_data/val_data.csv",
        ]
    )
    df["day_of_week"] = pd.Categorical(
        df["day_of_week"],
        categories=[
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
        ordered=True,
    )
    summary_stats(df)
    graph_time(df)
    numerical_boxplots(df)
    geographic_plots(df, "../10_original_data/community_areas.geojson")
