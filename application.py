import streamlit as st
import os
import pandas as pd
from datetime import datetime as dt
import cufflinks as cf
import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
from  plotly.subplots import make_subplots
from process import Process


## Application Logic ##
st.set_page_config(layout="centered")
st.sidebar.title("Konfiguracija")
select = st.sidebar.text("Regija: Bosna i Hercegovina")

data, fbih, rs, bd = 0, 0, 0, 0
startDate, endDate = 0, 0
filtered = 0

st.markdown("<h3 style = 'text-align: left;'>Podaci za Bosnu i Hercegovinu</h3>", unsafe_allow_html=True)
data = Process.Import("cleanData.xlsx")

date = st.sidebar.slider(
    "Odaberi vremenski opseg:",
    value = (dt.strptime(data['date'][0], "%d.%m.%Y"), dt.strptime(data.date[len(data.date) - 1], "%d.%m.%Y")),
    min_value = dt.strptime(data['date'][0], "%d.%m.%Y"),
    max_value = dt.strptime(data.date[len(data.date) - 1], "%d.%m.%Y"),
    format = "MM.DD.YY")

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
    st.plotly_chart(Process.SingleLinePlot(filtered, ['date', 'new_cases'], "Broj novih slučajeva korona virusa u Bosni i Hercegovini", ["Datum", "Slučajevi"]))
    st.plotly_chart(Process.SingleLinePlot(filtered, ['date', 'Testirani'], "Broj testiranih osoba u Bosni i Hercegovini", ["Datum", "Testirani"]))
    st.plotly_chart(Process.SingleLinePlot(filtered, ['date', 'Smrtni sl.'], "Broj smrtnih slučajeva uzrokovani COVID-om u Bosni i Hercegovini", ["Datum", "Smrtni slučajevi"]))
    st.plotly_chart(Process.SingleLinePlot(filtered, ['date', 'Oporavljeni'], "Broj oporavljenih osoba u Bosni i Hercegovini", ["Datum", "Oporavljene osobe"]))

    st.markdown("<br>", unsafe_allow_html = True)
    st.markdown("<br>", unsafe_allow_html = True)

metrics = pd.DataFrame()

metrics['date'] = filtered.date
metrics['testirani_slucaj'] = (filtered['new_cases'] / filtered['Testirani']) * 100
metrics['smrt_slucaj'] = (filtered['Smrtni sl.'] / filtered['Testirani']) * 100

showMetrics = st.checkbox("Prikaži preračunate podatke", True)
if showMetrics:
    st.plotly_chart(Process.SingleLinePlot(metrics, ['date', 'testirani_slucaj'], "Procent pozitivnih osoba u okviru testiranih osoba", ['Datum', 'Procent']))
    
    averagePositive = sum(filtered['new_cases']) / sum(filtered['Testirani'])
    averageTested = sum(filtered['Testirani']) / 3280815

    CT1, CT2 = st.beta_columns([7,1])
    CT3, CT4 = st.beta_columns([7,1])

    CT1.warning("Prosječan stopa zaraženosti u odnosu na broj testiranih je:")
    CT2.error(f"{averagePositive:.2%}")

    CT3.warning("Stopa testiranja stanovništva u Bosni i Hercegovini")
    CT4.error(f"{averageTested:.2%}")


    st.plotly_chart(Process.SingleLinePlot(metrics, ['date', 'smrt_slucaj'], "Procent smrtnosti okviru testiranih osoba", ['Datum', 'Procent']))
    C1, C2 = st.beta_columns([8,1])

    averageDeath = (sum(filtered['Smrtni sl.']) / sum(filtered['new_cases']))
    C1.warning("Prosječna smrtnost od COVID-19 u Bosni i Hercegovini je:")
    C2.error(f"{averageDeath:.2%}") 

st.sidebar.error("Format datuma je (mm.dd.gggg)")
st.sidebar.info("""O projektu možete saznati više na [GitHub](https://github.com/WorldWideWest/COVID-19)""")


