# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 22:58:33 2023

@author: Hasnain
"""

import pandas as pd
import numpy as np
import streamlit as st
#import matplotlib.pyplot as plt
st.set_page_config(layout="wide")

SHEET_ID_ATHLETE = '1n6ZVKylpKBgwZ1wA7LYZ1g-McGwyRlRSTYcbY9mmFxk'
SHEET_ID_REGION = '1nQJcG5UJ_pK08AnPMgy5U7yJCc_gefKwrV-RXf1z1qg'
#Reference link: https://medium.com/geekculture/2-easy-ways-to-read-google-sheets-data-using-python-9e7ef366c775
        
url1 = f'https://docs.google.com/spreadsheets/d/{SHEET_ID_ATHLETE}/gviz/tq?tqx=out:csv'
url2 = f'https://docs.google.com/spreadsheets/d/{SHEET_ID_REGION}/gviz/tq?tqx=out:csv'

#file1 = r'C:\Users\Lenovo\Desktop\Class 1 Python\Assignments\3rd Assignment\archive (1)\athlete_events.csv'
df1 = pd.read_csv(url1)

#file2 = r'C:\Users\Lenovo\Desktop\Class 1 Python\Assignments\3rd Assignment\archive (1)\noc_regions.csv'
df2 = pd.read_csv(url2)

data = pd.merge(df1, df2)
#data.isna().any()

data.info()
#df = data.drop(['notes'],axis=1)
st.header('Olympic History Dashboard')
Years = data['Year'].unique()
#selection = st.multiselect('Select Year', Years)

st.sidebar.header("Select Filters:")
selection = st.multiselect(
    "Select Year:",
        options = Years,
        default = Years)

Type = st.sidebar.multiselect(
    "Select Season:",
        options = data["Season"].unique(),
        default = data["Season"].unique())

#selection = st.multiselect(
#    "Select Year:",
#        options = Years,
#        default = Years)
subset = data[data['Year'] == selection]
drop_data = data.loc[:, ~data.columns.isin(['ID', 'notes'])]

subset1 = drop_data.query("Year == @selection")
subset = data.query("Year == @selection")

total_participations = subset['ID'].count()
total_olympians = subset['ID'].nunique()
countries = subset['NOC'].nunique()
gold = subset.Medal.value_counts().Gold
silver = subset.Medal.value_counts().Silver
bronze = subset.Medal.value_counts().Bronze


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric('Number of Participations', total_participations)
col2.metric('Number of Olympians', total_olympians)
col3.metric('Gold Medals', gold)
col4.metric('Silver Medals', silver)
col5.metric('Bronze Medals', bronze)

bar_data = subset.groupby('Medal')['Name'].count().sort_values(ascending=False).head(10)
#line_data = subset.groupby('Year')['Medal'].count().sort_values(ascending=False).head(10)
line_data = pd.crosstab(subset['Year'], subset['Medal'])

#st.dataframe(line_data)
with st.container():
    left, right = st.columns(2)
    right.header('No. of Medals by Year')
    right.line_chart(line_data)
    
    left.header('Medals Won by No. of Participations')
    left.bar_chart(bar_data)
        
st.header('Overall View')
st.dataframe(subset1)
       
   #left.header('Area Chart Visual')
   #left.area_chart(subset)
