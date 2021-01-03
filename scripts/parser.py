import pandas as pd
import os

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH = "/mnt/c/Program Files (x86)/msedgedriver.exe"

driver = webdriver.Edge(PATH)

driver.get("https://ourworldindata.org/coronavirus#coronavirus-country-profiles")

search = driver.find_element_by_id("react-select-2-input")
search.send_keys("Bosnia and Herzegovina")
search.send_keys(Keys.RETURN)


#rawData = pd.read_excel(os.path.join("../dataSet/rawData/", "mbih.xlsx"), engine='openpyxl')
#rawData = rawData[rawData['location'] == 'Bosnia and Herzegovina']
#rawData = rawData.dropna(axis = 1)
#rawData = rawData.drop(
#    ['iso_code', 'continent', 'location', 'total_cases_per_million', 'new_cases_per_million','aged_70_older','gdp_per_capita', 'extreme_poverty', 'cardiovasc_death_rate','diabetes_prevalence', 'female_smokers', 'male_smokers', 'handwashing_facilities', 'hospital_beds_per_thousand', 'life_expectancy', 'human_development_index'], axis = 1)

#rawData.to_excel(os.path.join("../dataSet/rawData/", "mbih.xlsx"))


