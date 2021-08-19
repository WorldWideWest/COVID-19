## Library import ##
import os
import numpy as np
import pandas as pd

## Data import ##
rawData = pd.read_excel(os.path.join("../dataSet/rawData/", "intBH.xlsx"), engine='openpyxl') # Data from ourworldindata.com
rawData['date'] = rawData['date'].astype('datetime64')
rawData['date'] = rawData['date'].dt.strftime('%d.%m.%Y')

bih = pd.read_excel(os.path.join("../dataSet/rawData/", "locBH.xlsx"), engine='openpyxl') # Data from local agencies

## Extracting data ##


def GetDay(dataFrame, column, newColumn, columnIndex):
    data = pd.DataFrame(columns = ["Datum", f"{newColumn}"])

    for index in range(0, len(dataFrame[f"{column}"])):    
        if index == len(dataFrame[f"{column}"]) - 2:
            i, j = index, len(dataFrame[f"{column}"]) - 1
        
            data = data.append(
                {"Datum": str(dataFrame.iloc[index, 0]), f"{newColumn}": int(dataFrame.iloc[i, columnIndex] - dataFrame.iloc[j, columnIndex ])},
                ignore_index = True)
            break
        else:
            i, j = index, index + 1
            data = data.append(
                {"Datum": str(dataFrame.iloc[index, 0]), f"{newColumn}": int(dataFrame.iloc[i, columnIndex] - dataFrame.iloc[j, columnIndex])},
                ignore_index = True)
    return data


tested = GetDay(bih, "Broj testiranih", "Testirani", 2)
recovered = GetDay(bih, "Broj oporavljenih osoba", "Oporavljeni", 4)
died = GetDay(bih, "Broj smrtnih slučajeva", "Smrtni sl.", 3)


fullDataFrame = pd.merge(left = rawData, left_on = 'date', how = 'left',
         right = recovered[['Oporavljeni', 'Datum']], right_on = 'Datum').drop('Datum', axis = 1)

fullDataFrame = pd.merge(left = fullDataFrame, left_on = 'date', how = 'left',
                        right = tested[['Datum', 'Testirani']], right_on = 'Datum').drop('Datum', axis = 1)

fullDataFrame = pd.merge(left = fullDataFrame, left_on = 'date', how = 'left',
                        right = died[['Datum', 'Smrtni sl.']], right_on = 'Datum').drop('Datum', axis = 1)


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
missingData.to_excel(os.path.join("../dataSet/cleanData/", "missingDataValues.xlsx"), index = False)
