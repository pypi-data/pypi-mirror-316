# trajectory_processing/filtering.py

import numpy as np
from scipy.interpolate import CubicSpline

def interpolate_cubic_spline_by_index(series):
    """
    使用三次样条插值填充缺失值。
    """
    valid_indices = series[~np.isnan(series)].index
    valid_values = series[~np.isnan(series)]

    if len(valid_indices) < 2:
        return series.fillna(np.nan)

    x_vals = np.array(valid_indices, dtype=float)
    spline = CubicSpline(x_vals, valid_values)
    all_indices = np.arange(len(series))
    interpolated_values = spline(all_indices)
    return pd.Series(interpolated_values, index=series.index)

def Median_filtering(data, step):
    """
    对经纬度数据进行中值滤波。
    """
    long = len(data)
    for i in range(step, long - step):
        a = data.iloc[i-step:i+step+1].sort_values(by='经度')
        data.at[i, '经度'] = a.iloc[step][data.columns.get_loc('经度')]
        b = data.iloc[i-step:i+step+1].sort_values(by='纬度')
        data.at[i, '纬度'] = b.iloc[step][data.columns.get_loc('纬度')]
    return data
