# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 08:12:22 2025

@author: nickwork
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.dates as mdates

import data_processing

def generate_grouped_plot(df,date_col,value_col,player):
    def grab_plot_elements(metric):
        # Function for generating plot title, axis titles, etc.
        input_metrics = {'Bat Speed':['bat_speed',f"{player}'s Bat Speed By Date",'Bat Speed (mph)'],
                         'Swing Length':['swing_length',f"{player}'s Swing Length By Date", 'Swing Length (ft)'],
                         'Attack Angle':['attack_angle', f"{player}'s Attack Angle By Date", 'Attack Angle (deg)'],
                         'Attack Direction':['attack_direction',f"{player}'s Attack Direction By Date", 'Attack Direction (deg)'],
                         'Swing Path Tilt':['swing_path_tilt',f"{player}'s Swing Path Tilt By Date", 'Swing Path Tilt (deg)']}
        return input_metrics[metric][0],input_metrics[metric][1], input_metrics[metric][2]
    value, plot_title, yax_label = grab_plot_elements(value_col)
    def group_data(df,group,value):
        # Grouping function to turn pitch-level data into outing-level data
        return (df.groupby(group).agg(daily_avg = (value,'mean'),
                                      daily_min = (value,'min'),
                                      daily_max = (value,'max'),
                                      percentile_25 = (value, lambda x: np.percentile(x, 0.25)),
                                      percentile_75 = (value, lambda x: np.percentile(x, 0.75))))
    df[date_col] = pd.to_datetime(df[date_col])
    _group_df = group_data(df,group = date_col, value = value)
    _group_df.index = pd.to_datetime(_group_df.index)
    fig,ax = plt.subplots(figsize = (16,10))
    ax.fill_between(_group_df.index,_group_df['daily_min'],_group_df['daily_max'],
                    color='#f5e6d3',alpha=0.7,label='Daily Range') # Calculate daily max/min for each metric
    ax.plot(_group_df.index,_group_df['daily_avg'],color='black',linewidth=1.5,label = f"Daily Average {value_col}") # metric should be replaced with checkbox value
    def clean_plot(_group_df, ax, plot_title, yax_title):
        # Format x-axis dynamically based on data range
        data_range = (_group_df.index.max() - _group_df.index.min()).days
        plt.yticks(fontsize=14)
        if data_range <= 7:  # 7 days or less - show daily
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            ax.xaxis.set_minor_locator(mdates.DayLocator())
            plt.xticks(rotation=90,fontsize=14)
        elif data_range <= 31:  # About a month - show days
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            ax.xaxis.set_minor_locator(mdates.DayLocator())
            plt.xticks(rotation=90, fontsize=14)
        elif data_range <= 90:  # About 3 months - show weeks
            ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))  # Mondays
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            ax.xaxis.set_minor_locator(mdates.DayLocator())
            plt.xticks(rotation=90, fontsize=14)
        elif data_range <= 365:  # Up to a year - show months
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%B'))
            ax.xaxis.set_minor_locator(mdates.WeekdayLocator())
            plt.xticks(rotation=90, fontsize=14)
        else:  # More than a year - show months with year
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            ax.xaxis.set_minor_locator(mdates.MonthLocator())
            plt.xticks(rotation=90, fontsize=14)

        # Set x-axis limits to match data exactly
        ax.set_xlim(_group_df.index.min(), _group_df.index.max())
        ax.legend(fontsize=16)
        ax.set_title(plot_title, fontsize=24)
        ax.set_ylabel(yax_title, fontsize=16)
        ax.set_xlabel("Date", fontsize=16)
        
        #Identify Lowest and highest values
        lowest_days = data_processing.return_extreme_values(_group_df, percentile = 5, n = 2)
        highest_days = data_processing.return_extreme_values(_group_df,percentile = 95, n = 2)
        for idx in lowest_days:
            ax.plot(_group_df.index[idx],_group_df['daily_avg'].iloc[idx],'o',color='blue',markersize=10)
        for idx in highest_days:
            ax.plot(_group_df.index[idx],_group_df['daily_avg'].iloc[idx],'o',color='red',markersize=10)
        return ax
    ax = clean_plot(_group_df, ax, plot_title, yax_label)
    return fig, ax
