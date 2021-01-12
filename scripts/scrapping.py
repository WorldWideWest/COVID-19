import os
import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup 
from datetime import datetime, timedelta

url = "http://www.mcp.gov.ba/publication/read/epidemioloska-slika-covid-19?pageId=3"
url2 = "http://www.mcp.gov.ba/publication/read/epidemioloska-slika-novo?pageId=3"

def Scrape(url):

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

    return tables

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
                
                    date = datetime.strptime(entity[0], "%d.%m.%Y")

                    cDate = datetime.strptime("26.8.2020", "%d.%m.%Y")
                    scDate = datetime.strptime("21.5.2020", "%d.%m.%Y")
                    tcDate = datetime.strptime("13.4.2020", "%d.%m.%Y")

                    if date > cDate:
                        for item in table[startIndex : endIndex]:
                            item = item.replace("*", "")
                            item = item.replace(" ", "")
                            entity.append(int(item))

                        entity.insert(6, 0)
                        formated.append(entity)

                    elif date > scDate:
                        for item in table[startIndex : endIndex]:
                            item = item.replace("*", "")
                            item = item.replace(" ", "")
                            entity.append(int(item))
                    
                        entity.insert(5, 0)
                        entity.insert(6, 0)
                        formated.append(entity)

                    elif scDate >= date and date > tcDate:
                        for item in table[startIndex : endIndex]:
                            item = item.replace("*", "")
                            item = item.replace(" ", "")
                            entity.append(int(item))

                        entity.insert(6, 0)
                        entity.insert(7, entity[3])
                        del entity[3]
                        formated.append(entity)

                    elif tcDate >= date:
                        for item in table[startIndex : endIndex]:
                            item = item.replace("*", "")
                            item = item.replace(" ", "")
                            entity.append(int(item))

                        entity.insert(5, 0)
                        entity.insert(6, 0)
                        entity.insert(7, entity[3])
                        del entity[3]
                        formated.append(entity)


   # 26.08.20
   # columns = ['Datum','Potvrđeni slučajevi', 'Broj testiranih', 'Broj smrtnih slučajeva', 'Broj oporavljenih osoba', 'Broj aktivnih slučajeva']
    # 25.08.20
   # columns = ['Datum','Potvrđeni slučajevi', 'Broj testiranih', 'Broj smrtnih slučajeva', 'Broj oporavljenih osoba']
    # 21.05.20
        columns = ['Datum','Potvrđeni slučajevi', 'Broj testiranih', 'Broj smrtnih slučajeva', 'Broj oporavljenih osoba', 'Broj aktivnih slučajeva',  'Broj osoba pod nadzorom']


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
                endIndex = len(table)
            elif len(table) == index + 1:
                 date = datetime.strptime(entity[0], "%d.%m.%Y")

                 cDate = datetime.strptime("26.8.2020", "%d.%m.%Y")
                 scDate = datetime.strptime("21.5.2020", "%d.%m.%Y")
                 tcDate = datetime.strptime("13.4.2020", "%d.%m.%Y")

                 if date > cDate:
                     for item in table[startIndex : endIndex]:
                         item = item.replace("*", "")
                         item = item.replace(" ", "")
                         entity.append(int(item))

                     entity.insert(6, 0)
                     formated.append(entity)

                 elif date > scDate:
                     for item in table[startIndex : endIndex]:
                         item = item.replace("*", "")
                         item = item.replace(" ", "")
                         entity.append(int(item))
                    
                     entity.insert(5, 0)
                     entity.insert(6, 0)
                     formated.append(entity)

                 elif scDate >= date and date > tcDate:
                     for item in table[startIndex : endIndex]:
                         item = item.replace("*", "")
                         item = item.replace(" ", "")
                         entity.append(int(item))

                     entity.insert(6, 0)
                     entity.insert(7, entity[3])
                     del entity[3]
                     formated.append(entity)

                 elif tcDate >= date:
                     for item in table[startIndex : endIndex]:
                         item = item.replace("*", "")
                         item = item.replace(" ", "")
                         entity.append(int(item))

                     entity.insert(5, 0)
                     entity.insert(6, 0)
                     entity.insert(7, entity[3])
                     del entity[3]
                     formated.append(entity)


    columns = ['Datum','Potvrđeni slučajevi', 'Broj testiranih', 'Broj smrtnih slučajeva', 'Broj oporavljenih osoba', 'Broj aktivnih slučajeva',  'Broj osoba pod nadzorom']

    dataFrame = pd.DataFrame(
        columns = columns,
        data = formated
    )
    return dataFrame

#### Parssing ####

bih2020 = Scrape(url)
bih2021 = Scrape(url2)

bih = getData("BiH", "RS", bih2020) 
rs = getData("RS", "FBiH", bih2020)
fbih = getData("FBiH", "BD", bih2020)
bd = getDataBD(bih2020)

bih1 = getData("BiH", "RS", bih2021) 
rs1 = getData("RS", "FBiH", bih2021)
fbih1 = getData("FBiH", "BD", bih2021)
bd1 = getDataBD(bih2021)

bih = pd.concat([bih, bih1])
rs = pd.concat([rs, rs1])
fbih = pd.concat([fbih, fbih1])
bd = pd.concat([bd, bd1])


## Saving data to excel ##

bih.to_excel("../dataSet/rawData/bih.xlsx", index = False)
rs.to_excel("../dataSet/rawData/rs.xlsx", index = False)
fbih.to_excel("../dataSet/rawData/fbih.xlsx", index = False)
bd.to_excel("../dataSet/rawData/bd.xlsx", index = False)

