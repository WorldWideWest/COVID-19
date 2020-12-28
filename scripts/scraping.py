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
for t in tables:
   print(t)
