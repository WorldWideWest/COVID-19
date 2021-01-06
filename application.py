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

## Functions ##
def Import(fileName, path = "dataSet/cleanData/"):
    return pd.read_excel(os.path.join(path, str(fileName)), engine = "openpyxl")


## Visualizing the missing data ##

dataFrame = Import(fileName = "missingData.xlsx")


availableData = [item for item in dataFrame.count()]
missingData = [item for item in dataFrame.isnull().sum()]

missingData = pd.DataFrame({
    "Column Name": dataFrame.columns,
    "Available Data": availableData,
    "Missing Data": missingData})


fig = go.Figure()

fig.add_trace(go.Bar(x = missingData["Column Name"], y = missingData["Available Data"],
                     marker_color = "#001024", name = "Available Data"))
fig.add_trace(go.Bar(x = missingData["Column Name"], y = missingData["Missing Data"],
                     marker_color = "#FF800B", name = "Missing Data"))

fig.update_layout(barmode='group', xaxis_tickangle=-45, title = "Missing Data for each Column of the Data Set", hovermode="x unified")

st.plotly_chart(fig)
