# trajectory_processing/span.py

import math
import pandas as pd


def Span(data: pd.DataFrame) -> pd.DataFrame:
    """
    计算两条轨迹之间的距离差。
    """
    R = 6371.393  # 地球半径，单位为千米

    data['距离差'] = 0  # 初始化
    for i in range(1, len(data)):
        lon_a, lat_a = data.iloc[i - 1, ['经度', '纬度']]
        lon_b, lat_b = data.iloc[i, ['经度', '纬度']]

        latA, lonA = math.radians(lat_a), math.radians(lon_a)
        latB, lonB = math.radians(lat_b), math.radians(lon_b)

        dlat = latB - latA
        dlon = lonB - lonA
        a = math.sin(dlat / 2) ** 2 + math.cos(latA) * math.cos(latB) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c * 1000  # 距离，单位为米
        data.at[i, '距离差'] = distance

    return data
