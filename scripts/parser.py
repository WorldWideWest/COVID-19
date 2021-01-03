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
#rawData = pd.read_excel(os.path.join("../dataSet/rawData/", "mbih.xlsx"), engine='openpyxl')
#rawData = rawData[rawData['location'] == 'Bosnia and Herzegovina']
#rawData = rawData.dropna(axis = 1)
#rawData = rawData.drop(
#    ['iso_code', 'continent', 'location', 'total_cases_per_million', 'new_cases_per_million','aged_70_older','gdp_per_capita', 'extreme_poverty', 'cardiovasc_death_rate','diabetes_prevalence', 'female_smokers', 'male_smokers', 'handwashing_facilities', 'hospital_beds_per_thousand', 'life_expectancy', 'human_development_index'], axis = 1)

#rawData.to_excel(os.path.join("../dataSet/rawData/", "mbih.xlsx"))


