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
    _hits = ['single','double','triple','home_run']
    _bases = _hits + ['walk']
    _at_bats = _hits + ['field_out','strikeout','grounded_into_double_play','double_play','force_out']
    _plate_appearances = _at_bats + ['walk']    
    _swings = ['foul','hit_into_play','swinging_strike']
    def calculate_batting_average(df, _hits, _at_bats):
        hits = df['events'].isin(_hits).sum()
        at_bats = df['events'].isin(_at_bats).sum()
        return hits / at_bats
    def calculate_OPS(df, _bases, _at_bats, _plate_appearances):
        def calculate_obp(df,_bases,_plate_appearances):
            bases = df['events'].isin(_bases).sum()
            plate_appearances = df['events'].isin(_plate_appearances).sum()
            return bases / plate_appearances
        def calculate_slug_pct(df, _at_bats):
            single_bases = df['events'].isin(['single']).sum()
            double_bases = df['events'].isin(['double']).sum() * 2
            triple_bases = df['events'].isin(['triple']).sum() * 3
            homerun_bases = df['events'].isin(['home_run']).sum() * 4
            at_bats = df['events'].isin(_at_bats).sum()
            return (single_bases + double_bases + triple_bases + homerun_bases) / at_bats
        obp = calculate_obp(df,_bases, _plate_appearances)
        slug_pct = calculate_slug_pct(df, _at_bats)
        ops = obp + slug_pct
        return obp, slug_pct, ops
    def calculate_chase_rate(df, _swings):
        _chase_zones = range(11,15,1)
        chases = df.loc[(df['description'].isin(_swings)) & (df['zone'].isin(_chase_zones))].shape[0]
        pitches = df.shape[0]
        return chases / pitches
    def calculate_whiff_rate(df, _swings):
        whiffs = df['description'].isin(['swinging_strike']).sum()
        swings = df['description'].isin(_swings).sum()
        return whiffs / swings
    batting_average = calculate_batting_average(df, _hits, _at_bats)
    obp, slug_pct, ops = calculate_OPS(df, _bases, _at_bats, _plate_appearances)
    chase_rate = calculate_chase_rate(df, _swings)
    whiff_rate = calculate_whiff_rate(df, _swings)
    metrics_dict = {'Batting Average': batting_average,
                    'On-Base Percentage': obp,
                    'Slugging Percentage': slug_pct,
                    'OPS': ops,
                    'Chase Rate': chase_rate,
                    'Whiff Rate': whiff_rate}
    return pd.DataFrame(metrics_dict, index = [0])