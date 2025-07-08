# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 08:07:07 2025

@author: nickwork
"""

import streamlit as st

pg = st.navigation([
    st.Page("team_selection.py",title='Team Selection'),
    st.Page("player_report.py",title='Player Report')])

pg.run()