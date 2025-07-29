# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 07:48:34 2025

@author: nickwork
"""

import streamlit as st
import matplotlib.pyplot as plt
import data_retrieval 
import data_visualization
import data_processing

if 'team_roster' not in st.session_state:
    st.stop()

with st.form("Batter Inputs Form"):
    player = st.selectbox('Select a batter:',options = st.session_state.team_roster['Player']) # Input is team roster derived from team_selection.py
    start_dt = st.date_input('Select the start date for analysis:',
                             value='today',
                             min_value = '2025-05-01',
                             max_value = 'today',
                             format = 'YYYY-MM-DD') # Dates used are cutoffs based on introduction of advanced batting metrics to statcast data
    end_dt = st.date_input('Select the end date for analysis:',
                           value='today',
                           min_value = '2025-05-01',
                           max_value = 'today',
                           format = 'YYYY-MM-DD')
    metrics = st.multiselect("Select the metrics you'd like to display:",
                             options = ['Bat Speed',
                                        'Swing Length',
                                        'Attack Angle',
                                        'Attack Direction',
                                        'Swing Path Tilt'])
    submitted = st.form_submit_button("Submit")
    if submitted:
        last_name = player.split()[1] # Pull players last name
        first_name = player.split()[0] # Pull players first name 
        start_dt = str(start_dt)
        end_dt = str(end_dt)
        player_id = data_retrieval.grab_player_id(last_name = last_name,first_name = first_name)
        df = data_retrieval.grab_batter_data(player_id = player_id, start_dt = start_dt, end_dt = end_dt)
        player_metrics = data_processing.calculate_batter_metrics(df)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label = 'Batting Average', value = player_metrics.loc[0,'Batting Average'].round(3))
            st.metric(label = 'OPS', value = player_metrics.loc[0,'OPS'].round(3))
        with col2:
            st.metric(label = 'On-Base Percentage', value = player_metrics.loc[0,'On-Base Percentage'].round(3))
            st.metric(label = 'Chase Rate', value = player_metrics.loc[0,'Chase Rate'].round(3))   
        with col3:
            st.metric(label = 'Slugging Percentage', value = player_metrics.loc[0,'Slugging Percentage'].round(3))
            st.metric(label = 'Whiff Rate', value = player_metrics.loc[0,'Whiff Rate'].round(3))                     
        for metric in metrics: # Iterate through list of selected metrics, generating plot for each one
            fig,ax = data_visualization.generate_grouped_plot(df, date_col = 'game_date', value_col = metric, player = player)
            st.pyplot(fig)
        st.snow()

    
