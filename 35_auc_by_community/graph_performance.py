"""Graph AUC by Pickup Area"""

import contextily as cx
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt


def graph(df: pd.DataFrame, model_name: str) -> None:
    """Graph data."""
    gdf = gpd.read_file("10_original_data/community_areas.geojson")
    total = gdf.merge(df, on="community", how="left")
    plt.rcParams.update({"font.size": 18})
    plt.rcParams.update({"font.size": 18})
    ax = total.plot(
        figsize=(15, 15),
        column="auc",
        cmap="RdYlGn",
        legend=True,
        legend_kwds={
            "shrink": 0.5,
            "label": "\nAUC Score",
        },
        alpha=0.8,
        edgecolor="#808080",
        missing_kwds=dict(color="grey", label="No Data"),
    )
    cx.add_basemap(ax, crs="EPSG:4326", source=cx.providers.CartoDB.Voyager)
    ax.set_axis_off()
    plt.savefig(
        f"26_images/graph_performance_{model}.png", bbox_inches="tight", dpi=400
    )


if __name__ == "__main__":
    pass
