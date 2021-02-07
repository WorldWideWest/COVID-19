import pandas as pd
import numpy as np
import os

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


def Merge(glob, arrays):
    dataFrame = glob[['date']]
    for array in arrays:
        dataFrame = pd.merge(left = dataFrame, left_on = 'date', how = 'left',
                            right = array, right_on = array.columns[0]).drop("Datum", axis = 1)

    return dataFrame

def Imputer(dataFrame):
    casesAvg =  int(sum(dataFrame.iloc[29:35, 1].values) / len(dataFrame.iloc[29:35, 1].values))
    startTestedAvg = int(sum(dataFrame.iloc[29:35, 2].values) / len(dataFrame.iloc[29:35, 2].values))
    startDiedAvg = int(sum(dataFrame.iloc[29:35, 3].values) / len(dataFrame.iloc[29:35, 3].values))

    for i in range(0, 29):
        dataFrame.iloc[i, 1] = casesAvg
        dataFrame.iloc[i, 2] = startTestedAvg
        dataFrame.iloc[i, 3] = startDiedAvg
        dataFrame.iloc[i, 4] = 0

    for colIndex, column in enumerate(dataFrame.columns):
        if column == "Oporavljeni" or column == "Testirani":
            for index in range(len(dataFrame[column])):
                if pd.isnull(dataFrame.iloc[index, colIndex]):
                    startIndex = index - 5
                    avgValue = int(sum(dataFrame.iloc[startIndex : index, colIndex]) / 5)
                    dataFrame.iloc[index, colIndex] = avgValue

        elif column == "Smrtni sl.":
            for index in range(len(dataFrame[column])):
                if pd.isnull(dataFrame.iloc[index, colIndex]):
                    startIndex = index - 2
                    avgValue = int(sum(dataFrame.iloc[startIndex : index, colIndex]) / 2)
                    dataFrame.iloc[index, colIndex] = avgValue

        elif column == "Slučajevi":
            for index in range(len(dataFrame[column])):
                if dataFrame.iloc[index, colIndex] == 0:
                    startIndex = index - 5
                    avgValue = int(sum(dataFrame.iloc[startIndex : index, colIndex]) / 5)
                    dataFrame.iloc[index, colIndex] = avgValue

                elif pd.isnull(dataFrame.iloc[index, colIndex]):
                    startIndex = index - 5
                    avgValue = int(sum(dataFrame.iloc[startIndex : index, colIndex]) / 5)
                    dataFrame.iloc[index, colIndex] = avgValue
    return dataFrame
## Importing Files ##


glob = pd.read_excel(os.path.join("../dataSet/rawData", "mbih.xlsx"), engine = "openpyxl")
glob['date'] = glob['date'].astype('datetime64')
glob['date'] = glob['date'].dt.strftime('%d.%m.%Y')

fbih = pd.read_excel(os.path.join("../dataSet/rawData", "fbih.xlsx"), engine = "openpyxl")
rs = pd.read_excel(os.path.join("../dataSet/rawData", "rs.xlsx"), engine = "openpyxl")
bd = pd.read_excel(os.path.join("../dataSet/rawData", "bd.xlsx"), engine = "openpyxl")


## FBIH ##
fbihSl = GetDay(fbih, "Potvrđeni slučajevi", "Slučajevi", 1)
fbihTest = GetDay(fbih, "Broj testiranih", "Testirani", 2)
fbihDied = GetDay(fbih, "Broj smrtnih slučajeva", "Smrtni sl.", 3)
fbihRec = GetDay(fbih, "Broj oporavljenih osoba", "Oporavljeni", 4)

fbih = Merge(glob, [fbihSl, fbihTest, fbihDied, fbihRec])
fbih = Imputer(fbih)

## RS ##
rsSl = GetDay(rs, "Potvrđeni slučajevi", "Slučajevi", 1)
rsTest = GetDay(rs, "Broj testiranih", "Testirani", 2)
rsDied = GetDay(rs, "Broj smrtnih slučajeva", "Smrtni sl.", 3)
rsRec = GetDay(rs, "Broj oporavljenih osoba", "Oporavljeni", 4)

rs = Merge(glob, [rsSl, rsTest, rsDied, rsRec])
rs = Imputer(rs)

## BD ##
bdSl = GetDay(bd, "Potvrđeni slučajevi", "Slučajevi", 1)
bdTest = GetDay(bd, "Broj testiranih", "Testirani", 2)
bdDied = GetDay(bd, "Broj smrtnih slučajeva", "Smrtni sl.", 3)
bdRec = GetDay(bd, "Broj oporavljenih osoba", "Oporavljeni", 4)

bd = Merge(glob, [bdSl, bdTest, bdDied, bdRec])
bd = Imputer(bd)

fbih.to_excel(os.path.join("../dataSet/cleanData", "fbih.xlsx"), index = False)
rs.to_excel(os.path.join("../dataSet/cleanData", "rs.xlsx"), index = False)
bd.to_excel(os.path.join("../dataSet/cleanData", "bd.xlsx"), index = False)

