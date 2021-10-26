import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from preprocessing import Preprocessing
from getpass import getuser
from datetime import date

today = str(date.today()).replace("-", "")

process = Preprocessing

url = "http://www.mcp.gov.ba/publication/read/epidemioloska-slika-covid-19?pageId=3"
url2 = "http://www.mcp.gov.ba/publication/read/epidemioloska-slika-novo?pageId=3"

#### Parssing ####

bih2020 = process.Scrape(url)
bih2021 = process.Scrape(url2)

bih = process.getData("BiH", "RS", bih2020) 
bih1 = process.getData("BiH", "RS", bih2021) 
bih = pd.concat([bih, bih1])

## Creating directories

# PATHS
mainPath, historyPath = "../dataSet/", "../dataSet/history/"

if not os.path.exists(mainPath):
    os.mkdir(mainPath)

if not os.path.exists(historyPath):
    os.mkdir(historyPath)

## Saving data from local government to excel ##
if os.path.isfile("../dataSet/locBH.xlsx"):
    os.rename("../dataSet/locBH.xlsx", f"../dataSet/history/locBH{ today }.xlsx")
    bih.to_excel("../dataSet/locBH.xlsx", index = False)
else:
    # os.rename("../dataSet/locBH.xlsx", f"../dataSet/history{ today }.xlsx")
    bih.to_excel("../dataSet/locBH.xlsx", index = False)

## Config ##
user = getuser()
directory = f"/home/{ user }/COVID-19/dataSet"

options = webdriver.ChromeOptions()
prefs = {'download.default_directory': directory}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options = options)


## Tasks 
website = "https://ourworldindata.org/coronavirus#coronavirus-country-profiles"
driver.get(website)

print(f"Found the website: { website }")

search = driver.find_element_by_id("react-select-2-input")
search.send_keys("Bosnia and Herzegovina")
search.send_keys(Keys.RETURN)

xslx = driver.find_element_by_partial_link_text(".xslx").click()
print("Successfuly started the download of the owid-covid-data.xlsx")

while not os.path.exists("../dataSet/owid-covid-data.xlsx"):
    time.sleep(1)
    print("The file is successfuly downloading")

if os.path.isfile("../dataSet/intBH.xlsx"):
    os.rename("../dataSet/intBH.xlsx", f"../dataSet/history/intBH{ today }.xlsx")
    os.rename("../dataSet/owid-covid-data.xlsx", "../dataSet/intBH.xlsx")

    print("All operations on the intBH.xlsx file are completed")
else:
    os.rename("../dataSet/owid-covid-data.xlsx", "../dataSet/intBH.xlsx")
    print("All operations on the intBH.xlsx file are completed")

driver.quit()

rawData = pd.read_excel(os.path.join("../dataSet/", "intBH.xlsx"), engine='openpyxl')
rawData = rawData[rawData['location'] == 'Bosnia and Herzegovina']
rawData = rawData.dropna(axis = 1)
rawData = rawData[["date", "total_cases", "new_cases", "population"]]
rawData.to_excel(os.path.join("../dataSet/", "rawIntBH.xlsx"), index = False)

print(f"All operations of scraping and downloading are completed successfuly and the file is available at: ../dataSet/rawIntBH.xlsx, locBH.xlsx")
