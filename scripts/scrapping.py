import os
import pandas as pd

from preprocessing import Preprocessing

process = Preprocessing

url = "http://www.mcp.gov.ba/publication/read/epidemioloska-slika-covid-19?pageId=3"
url2 = "http://www.mcp.gov.ba/publication/read/epidemioloska-slika-novo?pageId=3"

#### Parssing ####

bih2020 = process.Scrape(url)
bih2021 = process.Scrape(url2)

bih = process.getData("BiH", "RS", bih2020) 
rs = process.getData("RS", "FBiH", bih2020)
fbih = process.getData("FBiH", "BD", bih2020)
bd = process.getDataBD(bih2020)

bih1 = process.getData("BiH", "RS", bih2021) 
rs1 = process.getData("RS", "FBiH", bih2021)
fbih1 = process.getData("FBiH", "BD", bih2021)
bd1 = process.getDataBD(bih2021)

bih = pd.concat([bih, bih1])
rs = pd.concat([rs, rs1])
fbih = pd.concat([fbih, fbih1])
bd = pd.concat([bd, bd1])


## Saving data to excel ##

bih.to_excel("../dataSet/rawData/bih.xlsx", index = False)
rs.to_excel("../dataSet/rawData/rs.xlsx", index = False)
fbih.to_excel("../dataSet/rawData/fbih.xlsx", index = False)
bd.to_excel("../dataSet/rawData/bd.xlsx", index = False)

