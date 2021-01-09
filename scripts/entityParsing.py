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
                            right = array, right_on = array.columns[1]).drop("Datum", axis = 1)

    return dataFrame

## Importing Files ##


glob = pd.read_excel(os.path.join("../dataSet/rawData", "mbih.xlsx"), engine = "openpyxl")
fbih = pd.read_excel(os.path.join("../dataSet/rawData", "fbih.xlsx"), engine = "openpyxl")
rs = pd.read_excel(os.path.join("../dataSet/rawData", "rs.xlsx"), engine = "openpyxl")
bd = pd.read_excel(os.path.join("../dataSet/rawData", "bd.xlsx"), engine = "openpyxl")


## FBIH ##
fbihSl = GetDay(fbih, "Potvrđeni slučajevi", "Slučajevi", 1)
fbihTest = GetDay(fbih, "Broj testiranih", "Testirani", 2)
fbihDied = GetDay(fbih, "Broj smrtnih slučajeva", "Smrtni sl.", 3)
fbihRec = GetDay(fbih, "Broj oporavljenih osoba", "Oporavljeni", 4)

fbih = Merge(glob, [fbihSl, fbihTest, fbihDied, fbihRec])

## RS ##
rsSl = GetDay(rs, "Potvrđeni slučajevi", "Slučajevi", 1)
rsTest = GetDay(rs, "Broj testiranih", "Testirani", 2)
rsDied = GetDay(rs, "Broj smrtnih slučajeva", "Smrtni sl.", 3)
rsRec = GetDay(rs, "Broj oporavljenih osoba", "Oporavljeni", 4)

rs = Merge(glob, [rsSl, rsTest, rsDied, rsRec])

## BD ##
bdSl = GetDay(bd, "Potvrđeni slučajevi", "Slučajevi", 1)
bdTest = GetDay(bd, "Broj testiranih", "Testirani", 2)
bdDied = GetDay(bd, "Broj smrtnih slučajeva", "Smrtni sl.", 3)
bdRec = GetDay(bd, "Broj oporavljenih osoba", "Oporavljeni", 4)

bd = Merge(glob, [bdSl, bdTest, bdDied, bdRec])

print(fbih)
print(rs)
print(bd)
