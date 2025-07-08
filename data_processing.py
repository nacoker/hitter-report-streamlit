# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 08:28:20 2025

@author: nickwork
"""

import pandas as pd
import numpy as np

# This is meant to be used as a library of helper functions to appropriately 
# process the raw player df and return sub_dfs that will be used for plotting and report generation.

# Examples include: Filtering df to only ABs for calculating Batting Average, OBP, Chase, Whiff, etc.
# Filtering df to only swings for bat metrics like bat_speed, swing_path_tilt, etc.

def return_extreme_values(df, percentile, n = 2):
    if percentile <= 25:
        indices = np.where(df['daily_avg'] < np.percentile(df['daily_avg'], percentile))
    else:
        indices = np.where(df['daily_avg'] > np.percentile(df['daily_avg'], percentile))
    return indices[:n]

def calculate_batter_metrics(df): # Definitely not finished, but will be used to create either a figure or table. Possibly divide by pitch type.
    def calculate_batting_average(df):
        return None
    def calculate_OBP(df):
        return None
    def calculate_chase_rate(df):
        return None
    def calculate_whiff_rate(df):
        return None
    batting_average = calculate_batting_average(df)
    obp = calculate_OBP(df)
    chase_rate = calculate_chase_rate(df)
    whiff_rate = calculate_whiff_rate(df)
    metrics_dict = {'Batting Average': batting_average,
                    'On-Base Percentage': obp,
                    'Chase Rate': chase_rate,
                    'Whiff Rate': whiff_rate}
    return pd.DataFrame(metrics_dict)