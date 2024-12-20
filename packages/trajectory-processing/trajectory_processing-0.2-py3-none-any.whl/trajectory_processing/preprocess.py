import math
from trajectory_processing import utils  # 绝对导入
import os
import pandas as pd
import geopandas as gpd
from ptrail.core.TrajectoryDF import PTRAILDataFrame
from ptrail.features.kinematic_features import KinematicFeatures as spatial
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from datetime import datetime

# 设置 Matplotlib 配置
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 常量定义
file_dir = os.path.dirname(os.path.abspath(__file__))
GL_PROJ = "EPSG:32650"
AMENITIES_MEAN_AREA = 43092.96

def import_and_preprocess_excel(filepath: str) -> gpd.GeoDataFrame:
    df = pd.read_excel(filepath)
    df = df.rename(columns={
        "车牌": "user",
        "经度": "lon",
        "纬度": "lat",
        "gps时间戳": "time",
    })
    df["time"] = df["time"].apply(convert_to_iso8601)
    df["time"] = pd.to_datetime(df["time"])
    df = df.drop_duplicates(subset='time', keep='first')
    df = df.sort_values(by="time").reset_index(drop=True)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs=utils.GPS_CRS)
    gdf = utils.remove_outliers(gdf.to_crs(GL_PROJ)).to_crs(utils.GPS_CRS)
    gdf["track_id"] = utils.get_track_id(gdf)
    gdf = gdf.drop(columns=["geometry", "time_diff", "distance", "velocity"])
    float64_cols = gdf.select_dtypes(include=['float64']).columns.values
    gdf[float64_cols] = gdf[float64_cols].astype("float32")
    return gdf

def interpolate_cubic_spline_by_index(series):
    valid_indices = series[~np.isnan(series)].index
    valid_values = series[~np.isnan(series)]
    if len(valid_indices) < 2:
        return series.fillna(np.nan)
    x_vals = np.array(valid_indices, dtype=float)
    spline = CubicSpline(x_vals, valid_values)
    all_indices = np.arange(len(series))
    interpolated_values = spline(all_indices)
    interpolated_series = pd.Series(interpolated_values, index=series.index)
    return interpolated_series

def Median_filtering(data, step):
    long = len(data)
    step = step
    star_index = step
    end_index = long-step
    for i in range(star_index, end_index):
        a = data.iloc[i-step:i+step+1].sort_values(by='经度')
        data.at[i, '经度'] = a.iloc[step][data.columns.get_loc('经度')]
        b = data.iloc[i-step:i+step+1].sort_values(by='纬度')
        data.at[i, '纬度'] = b.iloc[step][data.columns.get_loc('纬度')]
    return data

def Span(data):
    R = 6371.393  # 地球半径，单位为千米
    for i in range(1, len(data)):
        lon_a, lat_a = data.iloc[i-1, [data.columns.get_loc('经度'), data.columns.get_loc('纬度')]]
        lon_b, lat_b = data.iloc[i, [data.columns.get_loc('经度'), data.columns.get_loc('纬度')]]
        latA, lonA = math.radians(lat_a), math.radians(lon_a)
        latB, lonB = math.radians(lat_b), math.radians(lon_b)
        dlat = latB - latA
        dlon = lonB - lonA
        a = math.sin(dlat/2)**2 + math.cos(latA) * math.cos(latB) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c * 1000  # 距离，单位为米
        data['距离差'][i] = distance
    return data

# 2024.12.4
def is_unix_timestamp(value):
    # 判断是否为 Unix 时间戳（一般为大于等于 1000000000 的数字）
    return isinstance(value, (int, float)) and value >= 1000000000


def convert_to_iso8601(value):
    # 判断是 Unix 时间戳还是已经是 ISO 8601 格式
    if is_unix_timestamp(value):  # 处理 Unix 时间戳
        return datetime.utcfromtimestamp(value / 1000).strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(value, str):  # 处理已是字符串格式的时间
        try:
            # 尝试解析 YYYY-MM-DD HH:MM:SS 格式
            datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return value  # 已经是正确的格式，直接返回
        except ValueError:
            raise ValueError(f"Invalid date format: {type(value)}")
    elif isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    else:
        raise ValueError(f"Unsupported value type: {value}")

def all(filepath):
    gdf = import_and_preprocess_excel(filepath)
    preproc_filepath = os.path.join(file_dir, "tmp")
    os.makedirs(preproc_filepath, exist_ok=True)
    csv_output_path = os.path.join(preproc_filepath, "processed_data.csv")
    gdf.to_csv(csv_output_path, index=False)
    df = pd.read_csv(csv_output_path)
    list_df = PTRAILDataFrame(data_set=df, datetime='time', traj_id='track_id', longitude='lon', latitude='lat', rest_of_columns=[])
    list_df = spatial.create_speed_column(list_df)
    list_df = spatial.create_bearing_column(list_df)
    list_df = list_df.reset_index(drop=True)
    new_column_names = {'lat': '纬度', 'lon': '经度', 'Speed': '速度', 'Bearing': '方向'}
    list_df.rename(columns=new_column_names, inplace=True)
    # 2024-12-2 处理每个轨迹id
    first_row_indices = list_df.index[list_df['轨迹id'] != list_df['轨迹id'].shift(1)]
    list_df = list_df.reset_index(drop=True)
    for idx in first_row_indices:
        current_id = list_df.loc[idx, '轨迹id']
        # 获取相同轨迹id的其余记录
        subset = list_df[list_df['轨迹id'] == current_id].iloc[1:]
        if not subset.empty:
            # 计算平均速度和方向
            avg_speed = subset['速度'].mean()
            avg_direction = subset['方向'].mean()
            avg_distance = subset['Distance'].mean()
            # 更新第一条记录的速度和方向
            list_df.loc[idx, ['Distance', '速度', '方向']] = avg_distance, avg_speed, avg_direction
    print('每条轨迹的起始值都设置为0成功')
    list_df['经度'] = interpolate_cubic_spline_by_index(list_df['经度'])
    list_df['纬度'] = interpolate_cubic_spline_by_index(list_df['纬度'])
    list_df = Median_filtering(list_df, step=2)
    list_df['前方向'] = list_df['方向'].shift(+1)
    list_df['前速度'] = list_df['速度'].shift(+1)
    list_df['前经度'] = list_df['经度'].shift(+1)
    list_df['前纬度'] = list_df['纬度'].shift(+1)
    list_df['距离差'] = np.NaN
    list_df = Span(list_df)
    list_df['定位时间'] = pd.to_datetime(list_df['定位时间'])
    list_df['时间差'] = list_df['定位时间'].diff().dt.total_seconds()
    list_df['时间差'] = list_df['时间差'].fillna(0).astype(int)
    list_df['year'] = list_df['定位时间'].dt.year
    list_df['month'] = list_df['定位时间'].dt.month
    list_df['day'] = list_df['定位时间'].dt.day
    list_df['hour'] = list_df['定位时间'].dt.hour
    list_df['minute'] = list_df['定位时间'].dt.minute
    list_df['second'] = list_df['定位时间'].dt.second
    list_df['加速度'] = (list_df['速度'] - list_df['前速度']) / list_df['时间差']
    list_df['速度'].fillna(0, inplace=True)
    list_df['前速度'].fillna(0, inplace=True)
    list_df['加速度'].fillna(0, inplace=True)
    columns_to_keep = ['user', '经度', '纬度', '轨迹id', '定位时间', 'Distance', '速度', '方向', '前方向', '前速度',
                       '前经度',
                       '前纬度', '距离差', '时间差', 'year', 'month', 'day', 'hour', 'minute', 'second', '加速度']
    list_df = list_df[columns_to_keep]
    list_df.to_csv(csv_output_path, index=False, encoding="gbk")
