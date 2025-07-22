# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 07:46:46 2025

@author: nickwork
"""

import mlbstatsapi
import statsapi
import streamlit as st
import pandas as pd

import data_retrieval

# Dict of all active MLB teams and team abbreviations
teams = {'AZ':'Arizona Diamondbacks','OAK':'Athletics',
         'ATL':'Atlanta Braves','BAL':'Baltimore Orioles',
         'BOS':'Boston Red Sox','CHC':'Chicago Cubs',
         'CWS':'Chicago White Sox','CIN':'Cincinnati Reds',
         'CLE':'Cleveland Guardians','COL':'Colorado Rockies',
         'DET':'Detroit Tigers','HOU':'Houston Astros',
         'KC':'Kansas City Royals','LAA':'Los Angeles Angels',
         'LAD':'Los Angeles Dodgers','MIA':'Miami Marlins',
         'MIL':'Milwaukee Brewers','MIN':'Minnesota Twins',
         'NYM':'New York Mets','NYY':'New York Yankees',
         'PHI':'Philadelphia Phillies','PIT':'Pittsburgh Pirates',
         'SD':'San Diego Padres','SF':'San Francisco Giants',
         'SEA':'Seattle Mariners','STL':'St. Louis Cardinals',
         'TB':'Tampa Bay Rays','TEX':'Texas Rangers',
         'TOR':'Toronto Blue Jays','WAS':'Washington Nationals'}

with st.form("Team Selection"):
    team = st.selectbox(label='Select an MLB team',options = teams.keys())
    submitted = st.form_submit_button(label='Submit')
    
if submitted:
    team_roster = data_retrieval.create_roster_df(data_retrieval.get_roster(teams[team])) 
    team_roster = team_roster.loc[team_roster['Position'] != 'P'] # Removes pitchers from roster
    st.dataframe(team_roster)
    st.session_state['team_roster'] = team_roster # Persist team roster by storing in session state
    st.switch_page("player_report.py")