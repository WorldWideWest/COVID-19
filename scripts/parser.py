import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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

