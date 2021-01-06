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
from plotly.subplots import make_subplot

## Functions ##
def Import(fileName, path = "../rawData/cleanData/"):
    return pd.read_excel(os.path.join(path, str(fileName)), engine = "openpyxl")


## Visualizing the missing data ##

missingData = Import(fileName = "missingData")

recovered = [fullDataFrame.isnull().sum()[4], fullDataFrame["Broj oporavljenih osoba"].count() - fullDataFrame.isnull().sum()[4]]
tested = [fullDataFrame.isnull().sum()[5], fullDataFrame["Broj testiranih dnevno"].count() - fullDataFrame.isnull().sum()[5]]
died = [fullDataFrame.isnull().sum()[6], fullDataFrame["Broj smrtnih slučajeva"].count() - fullDataFrame.isnull().sum()[6]]

names = ["Missing Values", "Present Values"]
colors = ["#FF800B", "#001024"]


## Missing percentage for Broj oporavljenih osoba
pct = fullDataFrame.isnull().sum()[4] / fullDataFrame["Broj oporavljenih osoba"].count()
pct = '{:.2%}'.format(pct)

## Missing percentage for Broj testiranih dnevno
pct1 = fullDataFrame.isnull().sum()[5] / fullDataFrame["Broj testiranih dnevno"].count()
pct1 = '{:.2%}'.format(pct1)

## Missing percentage for Broj smrtnih slučajeva  
pct2 = fullDataFrame.isnull().sum()[6] / fullDataFrame["Broj smrtnih slučajeva"].count()
pct2 = '{:.2%}'.format(pct2)


fig = make_subplots(
    rows = 1, cols = 3,
    specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],
    subplot_titles = ("Number of Recovered People", "Number of Tested People", "Number of Died"))

fig.add_trace(
    go.Pie(labels = names, values = recovered, hole = .8, textinfo = "none", text = [pct]),
    row = 1, col = 1)

fig.add_trace(
    go.Pie(labels = names, values = tested, hole = .8, textinfo = "none", text = [pct1]),
    row = 1, col = 2)

fig.add_trace(
    go.Pie(labels = names, values = died, hole = .8, textinfo = "none", text = [pct2],),
    row = 1, col = 3)

fig.add_annotation(x=0.1, y=0.5,
            text=pct,
            font_size=20,
            showarrow=False)

fig.add_annotation(x=0.5, y=0.5,
            text=pct1,
            font_size=20,
            showarrow=False)

fig.add_annotation(x=0.91, y=0.5,
            text=pct2,
            font_size=20,
            showarrow=False)

fig.update_traces(
    hoverinfo = 'label + value',
    marker = dict(colors = colors),
    col = 1
)

fig.update_traces(
    hoverinfo = 'label + value',
    marker = dict(colors = colors),
    col = 2
)

fig.update_traces(
    hoverinfo = 'label + value',
    marker = dict(colors = colors),
    col = 3
)
fig.update_layout(title_text="Missing Valus for the columns that are derived from the website of Ministry of Civil Affairs")

st.plotly_chart(fig.show())


