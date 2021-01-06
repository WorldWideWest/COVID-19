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
    
    data = []
    
 
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
st.markdown("<h1 style = 'text-align: center;'>COVID - 19 analysis in Bosnia and Herzegovina</h1>", unsafe_allow_html=True)


"""This analysis is based on data that is provided by Ministry of Civil Affairs and the ourworldindata, so we can create an overview of the COVID - 19 situation in Bosnia and Herzegovina."""

st.plotly_chart(fig)
