import os
import time
import logging as lg
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from preprocessing import Preprocessing

# Logging configuration 
lg.basicConfig(level = lg.INFO)

process = Preprocessing

url = "http://www.mcp.gov.ba/publication/read/epidemioloska-slika-covid-19?pageId=3"
url2 = "http://www.mcp.gov.ba/publication/read/epidemioloska-slika-novo?pageId=3"

#### Parssing ####

bih2020 = process.Scrape(url)
bih2021 = process.Scrape(url2)

bih = process.getData("BiH", "RS", bih2020) 
bih1 = process.getData("BiH", "RS", bih2021) 
bih = pd.concat([bih, bih1])


## Saving data to excel ##
bih.to_excel("../dataSet/rawData/locBH.xlsx", index = False)

## Config ##
directory = "/home/dzafo/COVID-19/dataSet/rawData"

options = webdriver.ChromeOptions()
prefs = {'download.default_directory': directory}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options = options)


## Tasks 
website = "https://ourworldindata.org/coronavirus#coronavirus-country-profiles"
driver.get(website)

lg.info(f"Found the website: { website }")

search = driver.find_element_by_id("react-select-2-input")
search.send_keys("Bosnia and Herzegovina")
search.send_keys(Keys.RETURN)

xslx = driver.find_element_by_partial_link_text(".xslx").click()
lg.info("Successfuly started the download of the owid-covid-data.xlsx")

while not os.path.exists("../dataSet/rawData/owid-covid-data.xlsx"):
    time.sleep(1)
    lg.info("The file is successfuly downloading")

if os.path.isfile("../dataSet/rawData/owid-covid-data.xlsx"):
    if os.path.isfile("../dataSet/rawData/intBH.xlsx"):

        os.remove("../dataSet/rawData/intBH.xlsx")
        os.rename("../dataSet/rawData/owid-covid-data.xlsx", "../dataSet/rawData/intBH.xlsx")
        lg.info("Deleted unnececary files and renemed the owid-covid-data.xlsx to intBH.xlsx")
    else:
        os.rename("../dataSet/rawData/owid-covid-data.xlsx", "../dataSet/rawData/intBH.xlsx")
        lg.info("Renemed the owid-covid-data.xlsx to intBH.xlsx")

driver.quit()

rawData = pd.read_excel(os.path.join("../dataSet/rawData/", "intBH.xlsx"), engine='openpyxl')
rawData = rawData[rawData['location'] == 'Bosnia and Herzegovina']
rawData = rawData.dropna(axis = 1)
rawData = rawData[["date", "total_cases", "new_cases", "population"]]
rawData.to_excel(os.path.join("../dataSet/rawData/", "intBH.xlsx"), index = False)

lg.info(f"All operations of scraping and downloading are completed successfuly and the file is available at: ../dataSet/rawData/intBH.xlsx, locBH.xlsx")
