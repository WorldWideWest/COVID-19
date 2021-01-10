import streamlit as st
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime as dt
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

def Plot(dataFrame, columns, title, labels):
    fig = px.line(dataFrame, x = f"{columns[0]}", y = f"{columns[1]}", title = f"{title}",
                  labels={
                      "sepal_lenght": labels[0],
                      "sepla_width": labels[1]
                  })
    fig.update_layout( width = 1300, height = 500)
    fig.update_traces(line_color = "#001024")
    return fig
## Application Logic ##

missingData = Import(fileName = "missingDataValues.xlsx")

fig = MissingDataPlot(missingData)
st.set_page_config(layout="centered")

select = st.sidebar.selectbox("Odaberite regiju:", ('Bosna i Hercegovina', 'Federacija Bosne i Hercegovine', 'Republika Srpska', 'Brčko Distrikt'))

data, fbih, rs, bd = 0, 0, 0, 0

startDate, endDate = 0, 0



if select == "Bosna i Hercegovina":
    st.markdown("<h3 style = 'text-align: left;'>Podaci za Bosnu i Hercegovinu</h3>", unsafe_allow_html=True)
    data = Import("cleanData.xlsx")

    
    date = st.sidebar.slider(
        "Odaberi vremenski opseg:",
        value = (dt.strptime(data['date'][0], "%d.%m.%Y"), dt.strptime(data.date[len(data.date) - 1], "%d.%m.%Y")),
        min_value = dt.strptime(data['date'][0], "%d.%m.%Y"),
        max_value = dt.strptime(data.date[len(data.date) - 1], "%d.%m.%Y"),
        format = "DD.MM.YY")


    startDate = dt.strftime(date[0], "%d.%m.%Y")
    endDate = dt.strftime(date[1], "%d.%m.%Y")

    print(data.info())
    print(startDate, endDate)
    
    show = st.checkbox("Prikaži podatke", True)
    if show:
        st.dataframe(data, height = 400, width = 850)
        st.markdown("<br>", unsafe_allow_html = True)
        st.markdown("<br>", unsafe_allow_html = True)
    
    


elif select == "Federacija Bosne i Hercegovine":
    fbih = Import('fbih.xlsx')
    st.markdown("<h3 style = 'text-align: left;'>Podaci za Federaciju BiH</h3>", unsafe_allow_html=True)
    st.dataframe(fbih, width = 840)
elif select == "Republika Srpska":
    rs = Import('rs.xlsx')
    st.markdown("<h3 style = 'text-align: left;'>Podaci za RS</h3>", unsafe_allow_html=True)
    st.dataframe(rs, width = 840)
elif select == "Brčko Distrikt":
    bd = Import('bd.xlsx')
    st.markdown("<h3 style = 'text-align: left;'>Podaci za Brčko Distrikt</h3>", unsafe_allow_html=True)
    st.dataframe(bd, width = 840)

























# st.markdown("<br>", unsafe_allow_html=True)
# st.markdown("<h1 id='datagethering' style = 'text-align: center;'>Data Visualization</h1>", unsafe_allow_html=True)

# """For the first part in this section will see the curve movement through time. To get litle bit of understanding how the pandemic has changed 
# over time."""
# daily = Plot(data, ['date', 'new_cases'], "Number of COVID - 19 Cases in Bosnia and Herzegovina", ["Date", "New Cases"])
# st.plotly_chart(daily)

# tested = Plot(data, ['date', 'Testirani'], "Number of tested people daily in Bosnia and Herzegovina", ["Date", "Tested"])
# st.plotly_chart(tested)
# # st.line_chart(data[["new_cases"]])
