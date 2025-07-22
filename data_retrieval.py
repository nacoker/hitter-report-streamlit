# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 08:36:34 2025

@author: nickwork
"""

from pybaseball import playerid_lookup, statcast_batter
import mlbstatsapi
import statsapi
import pandas as pd

def get_roster(team):
    # Function for using MLB Stats API to pull a team's active roster and return as a string
    mlb = mlbstatsapi.Mlb()
    team_id = mlb.get_team_id(team)[0]
    return statsapi.roster(team_id)

def create_roster_df(roster):
    # Function for taking roster string and parsing into a pandas dataframe
    lines = roster.strip().split('\n')
    rows = []
    for line in lines:
        parts = line.strip().split()
        number = int(parts[0].replace('#',''))
        position = parts[1]
        player = ' '.join(parts[2:])
        rows.append([number, position, player])
    return pd.DataFrame(rows,
                        columns=['Number',
                                 'Position',
                                 'Player'])
    
def grab_player_id(last_name,first_name):
    #Stores player id to be used for grab_batter_data
    return playerid_lookup(last=last_name,first=first_name).loc[0,'key_mlbam']

def grab_batter_data(player_id,start_dt,end_dt):
    #Returns df of pitch-level data for requested batter
    return statcast_batter(start_dt = start_dt,
                           end_dt = end_dt,
                           player_id = player_id)