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

def Covid(dataFrame, columns, title, labels):
    one, two = labels[0], labels[1]
    fig = px.line(dataFrame, x = f"{columns[0]}", y = f"{columns[1]}", title = f"{title}",
    labels=dict(date="Datum", new_cases="Broj solučajeva zaraze"))

    fig.update_layout(width = 700, height = 500)
    fig.update_traces(line_color = "#001024")
    return fig

def Tested(dataFrame, columns, title, labels):
    one, two = labels[0], labels[1]
    fig = px.line(dataFrame, x = f"{columns[0]}", y = f"{columns[1]}", title = f"{title}",
    labels=dict(date="Datum", Testirani="Broj testiranih osoba"))

    fig.update_layout(width = 700, height = 500)
    fig.update_traces(line_color = "#001024")
    return fig

def Recovered(dataFrame, columns, title, labels):
    fig = px.line(dataFrame, x = f"{columns[0]}", y = f"{columns[1]}", title = f"{title}",
    labels=dict(date="Datum", Oporavljeni="Broj oporavljenih osoba"))

    fig.update_layout(width = 700, height = 500)
    fig.update_traces(line_color = "#001024")
    return fig




## Application Logic ##

missingData = Import(fileName = "missingDataValues.xlsx")

st.set_page_config(layout="centered")

st.sidebar.title("Konfiguracija")
select = st.sidebar.selectbox("Odaberite regiju:", ('Bosna i Hercegovina', 'Federacija Bosne i Hercegovine', 'Republika Srpska', 'Brčko Distrikt'))

data, fbih, rs, bd = 0, 0, 0, 0

startDate, endDate = 0, 0

filtered = 0

if select == "Bosna i Hercegovina":
    st.markdown("<h3 style = 'text-align: left;'>Podaci za Bosnu i Hercegovinu</h3>", unsafe_allow_html=True)
    data = Import("cleanData.xlsx")

    date = st.sidebar.slider(
        "Odaberi vremenski opseg:",
        value = (dt.strptime(data['date'][0], "%d.%m.%Y"), dt.strptime(data.date[len(data.date) - 1], "%d.%m.%Y")),
        min_value = dt.strptime(data['date'][0], "%d.%m.%Y"),
        max_value = dt.strptime(data.date[len(data.date) - 1], "%d.%m.%Y"),
        format = "MM.DD.YY")
    
    st.sidebar.error("Format datuma je (mm.dd.gggg)")

    startDate, endDate = dt.strftime(date[0], "%m.%d.%Y"), dt.strftime(date[1], "%m.%d.%Y")
    data.date = pd.to_datetime(data.date, infer_datetime_format=True, dayfirst = True)

    filtered = data[(data.date >= startDate) & (data.date <= endDate)]

    show = st.checkbox("Prikaži podatke", True)
    if show:
        
        st.dataframe(filtered, height = 400, width = 850)
        st.markdown("<br>", unsafe_allow_html = True)
        st.markdown("<br>", unsafe_allow_html = True)

    showFigures = st.checkbox("Prikaži pojedinačne grafove (Broj novih slučajeva, testiranih, oporavljenih i smrtnih slučajeva)", True)
    if showFigures:
        st.plotly_chart(Covid(filtered, ['date', 'new_cases'], "Broj novih slučajeva korona virusa u Bosni i Hercegovini", ["Datum", "Slučajevi"]))
        st.plotly_chart(Tested(filtered, ['date', 'Testirani'], "Broj testiranih osoba u Bosni i Hercegovini", ["Datum", "Testirani"]))
        st.plotly_chart(Covid(filtered, ['date', 'Smrtni sl.'], "Broj smrtnih slučajeva uzrokovani COVID-om u Bosni i Hercegovini", ["Datum", "Testirani"]))
        st.plotly_chart(Recovered(filtered, ['date', 'Oporavljeni'], "Broj oporavljenih osoba u Bosni i Hercegovini", ["Datum", "Oporavljeni"]))

        st.markdown("<br>", unsafe_allow_html = True)
        st.markdown("<br>", unsafe_allow_html = True)

    metrics = pd.DataFrame()
    
    metrics['date'] = filtered.date
    metrics['testirani_slucaj'] = (filtered['new_cases'] / filtered['Testirani']) * 100
    metrics['smrt_slucaj'] = (filtered['Smrtni sl.'] / filtered['Testirani']) * 100
    
    showMetrics = st.checkbox("Prikaži preračunate podatke", True)
    if showMetrics:
        st.plotly_chart(Recovered(metrics, ['date', 'testirani_slucaj'], "Procent pozitivnih osoba u okviru testiranih osoba", ['Datum', 'Procent']))
        CT1, CT2 = st.beta_columns([8,1])
        CT1.info("")

        st.plotly_chart(Recovered(metrics, ['date', 'smrt_slucaj'], "Procent smrtnosti okviru testiranih osoba", ['Datum', 'Procent']))
        
        C1, C2 = st.beta_columns([8,1])

        averageDeath = (sum(filtered['Smrtni sl.']) / sum(filtered['new_cases']))
        C1.info("Prosječna smrtnost od COVID-19 u Bosni i Hercegovini predstavlja:")
        C2.error(f"{averageDeath:.2%}") 

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



