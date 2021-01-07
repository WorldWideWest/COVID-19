import streamlit as st
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import cufflinks as cf

import chart_studio.plotly as py
import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objects as go
from  plotly.subplots import make_subplots

## Functions ##
def Import(fileName, path = "dataSet/cleanData/"):
    return pd.read_excel(os.path.join(path, str(fileName)), engine = "openpyxl")

def MissingDataPlot(dataFrame):
    colors = ["#FF800B", "#001024"]
    names = ["Missing Values", "Present Values"]
    
    columns = [col for col in dataFrame["Column Name"]]
    
    specs = []
    
    for sp in range(len(columns)):
        specs.append({"type": "pie", "rowspan": 0})
    
    fig = make_subplots(rows = 1, cols = len(columns), specs = [specs], subplot_titles = columns)
    
    position = 0.03
    
    for index in range(len(missingData["Missing Data"])):
        move = 0.15
        avail = missingData.iloc[index, 2] 
        miss = missingData.iloc[index, 1]
        pct = missingData.iloc[index, 3]
    
        fig.add_trace(go.Pie(labels = names, values = [avail, miss], textinfo = "none", hole = .8),
                     row = 1, col = index + 1)
        
        if index == 0:
            fig.add_annotation(x = position, y=0.5, text="{:.2%}".format(pct), font_size = 15, showarrow = False)
            fig.update_traces(hoverinfo = 'label + value', marker = dict(colors = colors), col = index + 1)

        elif index <= 2:
            move = 0.15
            position += move
            fig.add_annotation(x = position, y=0.5, text="{:.2%}".format(pct), font_size = 15, showarrow = False)
            fig.update_traces(hoverinfo = 'label + value', marker = dict(colors = colors), col = index + 1)
          
        elif index == 3:
            move = 0.175
            position += move
            fig.add_annotation(x = position, y=0.5, text="{:.2%}".format(pct), font_size = 15, showarrow = False)
            fig.update_traces(hoverinfo = 'label + value', marker = dict(colors = colors), col = index + 1)
        elif index == 4:
            move = 0.14
            position += move
            fig.add_annotation(x = position, y=0.5, text="{:.2%}".format(pct), font_size = 15, showarrow = False)
            fig.update_traces(hoverinfo = 'label + value', marker = dict(colors = colors), col = index + 1)
        elif index == 5:
            move = 0.18
            position += move
            fig.add_annotation(x = position, y=0.5, text="{:.2%}".format(pct), font_size = 15, showarrow = False)
            fig.update_traces(hoverinfo = 'label + value', marker = dict(colors = colors), col = index + 1)
        elif index == 6:
            move = 0.15
            position += move
            fig.add_annotation(x = position, y=0.5, text="{:.2%}".format(pct), font_size = 15, showarrow = False)
            fig.update_traces(hoverinfo = 'label + value', marker = dict(colors = colors), col = index + 1)
        fig.update_layout(title_text="Procentage of Missing Values for Each Column in the Data Set", width = 1300, height = 500)
    return fig

## Application Logic ##

missingData = Import(fileName = "missingDataValues.xlsx")

fig = MissingDataPlot(missingData)
st.set_page_config(layout="wide")


st.sidebar.title('Navigation')
st.sidebar.markdown("<a style = 'a:link{text-decoration: none;}' href = '#home'>Home</a>", unsafe_allow_html=True)
st.sidebar.markdown("<a href = '#datagethering'>Data Gethering</a>", unsafe_allow_html=True)
st.sidebar.markdown("<a href = '#datagethering'>Data Visualization</a>", unsafe_allow_html=True)
st.sidebar.markdown("<a href = '#datagethering'>Metrics Calculation</a>", unsafe_allow_html=True)
st.sidebar.markdown("<a href = '#datagethering'>Recurent Neural Network</a>", unsafe_allow_html=True)

st.markdown("<h1 id='home' style = 'text-align: center;'>COVID - 19 analysis in Bosnia and Herzegovina</h1>", unsafe_allow_html=True)


"""This analysis will provide a complete overview of the COVID - 19 situation in Bosnia and Herzegovina. The first part of this analysis will be
based on the data that is gathered. Then will continue on visualizing the data and get a more complete overview of the situation. Keep in mind that
we have about 30% of missing data in the columns that are valuable to us so we must fill them somehow. The analysis will contain the entity's and
the District. To fulfill our analysis we must calculate some metrics and based on that make predictions for the future.""" 

st.markdown("<h1 id='datagethering' style = 'text-align: center;'>Data Gathering</h1>", unsafe_allow_html=True)
"""The data that we have here and will display it to you in the later part of this analysis is gathered from two webistes, the first website is
ourworldindata and the second website is the website of the Ministry of Civil Affairs.

From the first website we pulled the dates, the cases and the population, and from the second website we pulled number of people recovered, died and 
tested. The bigger problem to us was that the table structure on the second website made no sense every few days the structure of the tables
changed. Based on that we needed to adjust our scraping algorithm, because it was a plain html website we used BeautifulSoup to scrape the data
and for the ourworldindata as it was a webapp we used selenium to get our hands on the data."""

"""We are at the first part of the analysis and as we can see we have a lot of missing data in the columns that have the most value to us. Will
try to fix that using custom functions from sklearn library, but we need to be carefoul because we can't take the whole dataset and have an average
to fill the missing values because at the begining of the pandemic we have not had the same numbers as today."""
st.plotly_chart(fig)