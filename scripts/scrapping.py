import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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


## Config ##
PATH = "/mnt/c/Program Files (x86)/chromedriver.exe"

options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : 'C:\\Users\\Dzenan\\Documents\\PythonDevelopment\\COVID-19\\dataSet\\rawData'}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(PATH, chrome_options = options)


## Tasks 
driver.get("https://ourworldindata.org/coronavirus#coronavirus-country-profiles")

search = driver.find_element_by_id("react-select-2-input")
search.send_keys("Bosnia and Herzegovina")
search.send_keys(Keys.RETURN)

xslx = driver.find_element_by_partial_link_text(".xslx").click()

while not os.path.exists("../dataSet/rawData/owid-covid-data.xlsx"):
    time.sleep(1)

if os.path.isfile("../dataSet/rawData/owid-covid-data.xlsx"):
    if os.path.isfile("../dataSet/rawData/mbih.xlsx"):

        os.remove("../dataSet/rawData/mbih.xlsx")
        os.rename("../dataSet/rawData/owid-covid-data.xlsx", "../dataSet/rawData/mbih.xlsx")
        

driver.quit()
rawData = pd.read_excel(os.path.join("../dataSet/rawData/", "mbih.xlsx"), engine='openpyxl')
rawData = rawData[rawData['location'] == 'Bosnia and Herzegovina']
rawData = rawData.dropna(axis = 1)
rawData = rawData[["date", "total_cases", "new_cases", "population"]]
rawData.to_excel(os.path.join("../dataSet/rawData/", "mbih.xlsx"), index = False)

print("Task completed successfully, file is parsed and it's available at: ", os.path.join("../dataSet/rawData/", "mbih.xlsx"))
