import pandas as pd
import os 

dataFrame = pd.read_excel(os.path.join("../dataSet/", "rawData.xlsx"), engine = "openpyxl")


startTestedAvg = int(sum(dataFrame.iloc[29:35, 5].values) / len(dataFrame.iloc[29:35, 5].values))
startDiedAvg = int(sum(dataFrame.iloc[29:35, 6].values) / len(dataFrame.iloc[29:35, 6].values))

for i in range(0, 29):
    dataFrame.iloc[i, 4] = 0
    dataFrame.iloc[i, 5] = int(startTestedAvg)
    dataFrame.iloc[i, 6] = startDiedAvg

for colIndex, column in enumerate(dataFrame.columns):
    if column == "recovered" or column == "tested":
        for index in range(len(dataFrame[column])):
            if pd.isnull(dataFrame.iloc[index, colIndex]):
                startIndex = index - 5
                avgValue = int(sum(dataFrame.iloc[startIndex : index - 1, colIndex]) / 5)
                dataFrame.iloc[index, colIndex] = avgValue
            elif dataFrame.iloc[index, colIndex] < 0:
                startIndex = index - 5
                avgValue = int(sum(dataFrame.iloc[startIndex : index, colIndex]) / 5)
                dataFrame.iloc[index, colIndex] = avgValue

    elif column == "died":
        for index in range(len(dataFrame[column])):
            if pd.isnull(dataFrame.iloc[index, colIndex]):
                startIndex = index - 3
                avgValue = int(sum(dataFrame.iloc[startIndex : index - 1, colIndex]) / 3)
                dataFrame.iloc[index, colIndex] = avgValue
            elif dataFrame.iloc[index, colIndex] < 0:
                dataFrame.iloc[index, colIndex] = dataFrame.iloc[index, colIndex] * (-1)
 


    elif column == "new_cases":
        for index in range(len(dataFrame[column])):
            if dataFrame.iloc[index, colIndex] == 0:
                startIndex = index - 5
                avgValue = int(sum(dataFrame.iloc[startIndex : index - 1, colIndex]) / 5)
                dataFrame.iloc[index, colIndex] = avgValue

            elif pd.isnull(dataFrame.iloc[index, colIndex]):
                startIndex = index - 5
                avgValue = int(sum(dataFrame.iloc[startIndex : index - 1, colIndex]) / 5)
                dataFrame.iloc[index, colIndex] = avgValue
        
            elif dataFrame.iloc[index, colIndex] < 0:
                dataFrame.iloc[index, colIndex] = dataFrame.iloc[index, colIndex] * (-1)
 
                

for colIndex, column in enumerate(dataFrame.columns):
     if column == "recovered" or column == "tested":
        for index in range(len(dataFrame[column])):
            if dataFrame.iloc[index, colIndex] > 5000:
                startIndex = index - 5
                avgValue = int(sum(dataFrame.iloc[startIndex : index - 1, colIndex]) / 5)
                dataFrame.iloc[index, colIndex] = avgValue
            elif dataFrame.iloc[index, colIndex] == 0 and index > 28:
                startIndex = index - 5
                avgValue = int(sum(dataFrame.iloc[startIndex : index - 1, colIndex]) / 5)
                dataFrame.iloc[index, colIndex] = avgValue

dataFrame.to_excel(os.path.join("../dataSet/", "cleanData.xlsx"), index = False)
