from bs4 import BeautifulSoup 
import requests
from datetime import datetime
import re

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


## Table dimensions 0:31
start, end = 0, 0
tables = []

for index in range(len(rawTables)):
    table = []
    if index == 0:
        start = index
        end = index + 31
    else:
        start = end
        end = start + 31
    
    table = rawTables[start:end]
    for i, element in enumerate(table):
        if i == 0:
            match = re.search(r'\d{2}.\d{2}.\d{4}', element)
            table.remove(element)
            table.insert(0, match.group(0))
            tables.append(table)
        if i > 1:
            table.remove(element)
    break

for t in tables:
    print(t)
