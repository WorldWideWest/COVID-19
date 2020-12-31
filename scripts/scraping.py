import os
import wget
import pandas as pd
import numpy as np
import requests
import re
import sqlite3
from bs4 import BeautifulSoup 
from datetime import datetime

url = "http://mcp.gov.ba/Publication/Read/epidemioloska-slika-covid-19#"

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

rawTables = []

for i in soup.find_all("table"):
    rows = i.find_all("tr")
    
    for row in rows:
        data = row.find_all("td")
        for ind in data:
            rawTables.append(ind.text.strip())

elements, formated = [], []

for element in rawTables:
    pattern = re.compile(r'\d{2}.\d{2}.\d{4}')
    if pattern.match(element):
        if len(elements) > 0:
            elements = list(filter(None, elements))
            formated.append(elements)
            elements.clear()
        elements.append(element)
    else: 
        elements.append(element)

rawTables.clear()
elements.clear()

tables = []

for table in formated:
    for index, element in enumerate(table):
        pattern = re.compile(r'\d{2}.\d{2}.\d{4}')
        match = pattern.match(element)
        if match:
            table.remove(element)
            table.insert(0, match.group(0))
        elif len(table) == index + 1:
            table = list(filter(None, table))
            tables.append(table)
        else:
            pass

formated.clear()


#### Parssing the function  ####


#startIndex, endIndex = 0, 0
def getData(start, end, tables):
    formated = []
    for table in tables:
        startIndex, endIndex = 0, 0
        entity = []

        for index, element in enumerate(table):
       
            if index == 0:
                entity.append(element)
            elif element == f"{start}":
                startIndex = index + 1
            elif element == f"{end}":
                endIndex = index
            
                for item in table[startIndex : endIndex]:
                    item = item.replace("*", "")
                    item = item.replace(" ", "")
                    entity.append(int(item))
                formated.append(entity)
    columns = ['Datum','Potvrđeni slučajevi', 'Broj testiranih', 'Broj smrtnih slučajeva', 'Broj oporavljenih osoba', 'Broj aktivnih slučajeva']

    dataFrame = pd.DataFrame(
        columns = columns,
        data = formated
    )
    return dataFrame

def getDataBD(tables):
    formated = []
    for table in tables:
        startIndex, endIndex = 0, 0
        entity = []
        for index, element in enumerate(table):
            if index == 0:
                entity.append(element)
            elif element == "BD":
                startIndex = index + 1 
                endIndex = len(table) - 1
            elif len(table) == index + 1:
                for item in table[startIndex : endIndex]:
                    item = item.replace(" ", "")
                    item = item.replace("*", "")
                    entity.append(int(item))
                if len(entity) < 6:
                    entity.append(0)
                formated.append(entity)
    columns = ['Datum','Potvrđeni slučajevi', 'Broj testiranih', 'Broj smrtnih slučajeva', 'Broj oporavljenih osoba', 'Broj aktivnih slučajeva']

    dataFrame = pd.DataFrame(
        columns = columns,
        data = formated
    )
    return dataFrame

bih = getData("BiH", "RS", tables)
rs = getData("RS", "FBiH", tables)
fbih = getData("FBiH", "BD", tables)
bd = getDataBD(tables)


## Saving data to excel ##

bih.to_excel("../dataSet/rawData/bih.xlsx")
rs.to_excel("../dataSet/rawData/rs.xlsx")
fbih.to_excel("../dataSet/rawData/fbih.xlsx")
bd.to_excel("../dataSet/rawData/bd.xlsx")



