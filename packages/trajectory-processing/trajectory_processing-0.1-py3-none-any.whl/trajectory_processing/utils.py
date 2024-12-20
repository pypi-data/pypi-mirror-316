# utils.py

import geopandas as gpd
import pandas as pd
import numpy as np

# 函数: 去除异常值
def remove_outliers(gdf: gpd.GeoDataFrame, def_vel_treshhold: float = 400) -> pd.DataFrame:
    """
    Remove location outliers based on max velocity threshold (default 400 m/s).
    Depending on transportation mode (Dabiri & Heaslip, 2018)
    """
    assert not gdf.crs.utm_zone is None, "CRS is not in UTM format"
    len_before_iter = np.inf

    # while still outliers detected
    while (len(gdf) < len_before_iter):
        gdf = gdf.reset_index(drop=True)
        len_before_iter = len(gdf)
        # add additional columns
        gdf["time_diff"] = (gdf.time - gdf.time.shift(1)).dt.total_seconds()
        gdf["distance"] = gdf.geometry.distance(gdf.geometry.shift(1))
        gdf["velocity"] = gdf["distance"] / gdf.time_diff
        gdf.loc[0, ["time_diff", "distance", "velocity"]] = 0
        gdf = gdf[~(
                (gdf.velocity > def_vel_treshhold) &
                (gdf.velocity.shift(-1) > def_vel_treshhold)
            )]

    return gdf

def get_track_id(gdf: gpd.GeoDataFrame, time_thresh_split_sec: float = 20 * 60, def_vel_treshhold: float = 400):
    """
    Splits dataset into tracks by user, time and location. Velocity works here
    as jump detection between trajectory

    time_thresh_split_sec: Threshold to split trajectories in seconds, Moreau
    et al. (2021) and others used 20min
    """
    track_change = gdf.user != gdf.user.shift(1)
    track_change = track_change | (gdf.time_diff > time_thresh_split_sec)
    track_change = track_change | (gdf.velocity > def_vel_treshhold)
    return track_change.cumsum()
# 常量定义

GPS_CRS = "EPSG:4326"  # GPS坐标系
