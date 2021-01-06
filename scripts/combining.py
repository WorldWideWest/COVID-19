## Library import ##
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
from plotly.subplots import make_subplots


## Data import ##
rawData = pd.read_excel(os.path.join("../dataSet/rawData/", "mbih.xlsx"), engine='openpyxl')
rawData['date'] = rawData['date'].astype('datetime64')
rawData['date'] = rawData['date'].dt.strftime('%d.%m.%Y')

bih = pd.read_excel(os.path.join("../dataSet/rawData/", "bih.xlsx"), engine='openpyxl')

## Extracting data ##

tested = pd.DataFrame(columns = ["Datum", "Broj testiranih dnevno"])
recovered = pd.DataFrame(columns = ["Datum", "Broj oporavljenih osoba"])
died = pd.DataFrame(columns = ["Datum", "Broj smrtnih slučajeva"])

for index in range(0, len(bih["Broj testiranih"])):    
    if index == len(bih["Broj testiranih"]) - 2:
        i, j = index, len(bih["Broj testiranih"]) - 1
        
        tested = tested.append(
            {"Datum": str(bih.iloc[index, 0]), "Broj testiranih dnevno": bih.iloc[i, 2] - bih.iloc[j, 2]},
            ignore_index = True)
        
        break
    else:
        i, j = index, index + 1
        tested = tested.append(
            {"Datum": str(bih.iloc[index, 0]), "Broj testiranih dnevno": bih.iloc[i, 2] - bih.iloc[j, 2]},
            ignore_index = True)   


for index in range(0, len(bih["Broj oporavljenih osoba"])):    
    if index == len(bih["Broj testiranih"]) - 2:
        
        i, j = index, len(bih["Broj testiranih"]) - 1

        recovered = recovered.append(
            {"Datum": str(bih.iloc[index, 0]), "Broj oporavljenih osoba": bih.iloc[i, 4] - bih.iloc[j, 4]},
            ignore_index = True)
        
        break
    else:
        i, j = index, index + 1
        
        recovered = recovered.append(
            {"Datum": str(bih.iloc[index, 0]), "Broj oporavljenih osoba": bih.iloc[i, 4] - bih.iloc[j, 4]},
            ignore_index = True)

for index in range(0, len(bih["Broj smrtnih slučajeva"])):    
    if index == len(bih["Broj smrtnih slučajeva"]) - 1:
        i, j = index, len(bih["Broj smrtnih slučajeva"]) - 1
        
        died = died.append(
            {"Datum": str(bih.iloc[index, 0]), "Broj smrtnih slučajeva": bih.iloc[i, 3] - bih.iloc[j, 3]},
            ignore_index = True)
        
        break
    else:
        i, j = index, index + 1
        died = died.append(
            {"Datum": str(bih.iloc[index, 0]), "Broj smrtnih slučajeva": bih.iloc[i, 3] - bih.iloc[j, 3]},
            ignore_index = True)

fullDataFrame = pd.merge(left = rawData, left_on = 'date', how = 'left',
         right = recovered[['Broj oporavljenih osoba', 'Datum']], right_on = 'Datum').drop('Datum', axis = 1)

fullDataFrame = pd.merge(left = fullDataFrame, left_on = 'date', how = 'left',
                        right = tested[['Datum', 'Broj testiranih dnevno']], right_on = 'Datum').drop('Datum', axis = 1)

fullDataFrame = pd.merge(left = fullDataFrame, left_on = 'date', how = 'left',
                        right = died[['Datum', 'Broj smrtnih slučajeva']], right_on = 'Datum').drop('Datum', axis = 1)


availableData = [item for item in fullDataFrame.count()]
missingData = [item for item in fullDataFrame.isnull().sum()]
missingPct = []

for i,j in zip(availableData, missingData):
    missingPct.append(j/i)

missingData = pd.DataFrame({
    "Column Name": fullDataFrame.columns,
    "Available Data": availableData,
    "Missing Data": missingData,
    "Missing Pct": missingPct})




fullDataFrame.to_excel(os.path.join("../dataSet/cleanData/", "missingData.xlsx"), index = False)


