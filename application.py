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

def Plot(dataFrame):
    fig = px.line(dataFrame, x = "date", y = "new_cases", title = "Number of Cases each day in Bosnia and Herzegovina")
    fig.update_layout( width = 1300, height = 500)
    return fig
## Application Logic ##

missingData = Import(fileName = "missingDataValues.xlsx")

fig = MissingDataPlot(missingData)
st.set_page_config(layout="wide")


st.sidebar.title('Navigation')
st.sidebar.markdown("<a href = '#home'>Home</a>", unsafe_allow_html=True)
st.sidebar.markdown("<a href = '#datagethering'>Data Gethering and Preprocessing</a>", unsafe_allow_html=True)
st.sidebar.markdown("<a href = '#datagethering'>Data Visualization</a>", unsafe_allow_html=True)
st.sidebar.markdown("<a href = '#datagethering'>Metrics Calculation</a>", unsafe_allow_html=True)
st.sidebar.markdown("<a href = '#datagethering'>Recurent Neural Network</a>", unsafe_allow_html=True)

st.markdown("<h1 id='home' style = 'text-align: center;'>COVID - 19 analysis in Bosnia and Herzegovina</h1>", unsafe_allow_html=True)


"""This analysis will provide a complete overview of the COVID - 19 situation in Bosnia and Herzegovina. The first part of this analysis will be
based on the data that is gathered. Then will continue on visualizing the data and get a more complete overview of the situation. Keep in mind that
we have about 30% of missing data in the columns that are valuable to us so we must fill them somehow. The analysis will contain the entity's and
the District. To fulfill our analysis we must calculate some metrics and based on that make predictions for the future.""" 

st.markdown("<h1 id='datagethering' style = 'text-align: center;'>Data Gethering and Preprocessing</h1>", unsafe_allow_html=True)
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

"""Now that the data is layed out we need to fill the missing values. One way to fill the data would be to import as described a custom function
from sklearn, but we are not going to do that because there is a lot of missing data and in the case of the COVID pandemic we don't have the 
same values at the begining in the middle and now.

So we must be creative. The way we are going to aproach this problem is when ever we encounter a missing value we are going to take an average 
of the previous 5 days and take this as our new value. But there is one more problem we can't just do that with the number of died, we will lower
the number of days we calculate the average to 2 days. For the first days of the pandemic we are also missing data and for that we will take the 
average for the first 5 days that we have data and put it into the row at the begining of the pandemic.

Because we have missing data in the new cases column we will take the same approach to this task also and take a 5 day average to get the data
for the missing value. Now you can see our dataframe with no missing valus."""

data = Import('cleanData.xlsx')

st.dataframe(data, width = 1150)
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<h1 id='datagethering' style = 'text-align: center;'>Data Visualization</h1>", unsafe_allow_html=True)

"""For the first part in this section will see the curve movement through time. To get litle bit of understanding how the pandemic has changed 
over time."""
daily = Plot(data)
st.plotly_chart(daily)
# st.line_chart(data[["new_cases"]])
