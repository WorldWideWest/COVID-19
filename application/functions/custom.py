import requests
import pandas as pd


def get_data(url:str) -> object:
    pd.set_option('colheader_justify', 'center') 
    get = requests.get(url)
    dataFrame = pd.read_json(get.content)
    dataFrame = dataFrame[['date', 'total_cases', 'new_cases', 'recovered', 'tested', 'died']]
    
    dataFrame = dataFrame.rename(columns = {
        'date': 'Date', 'total_cases': 'Total Cases', 
        'new_cases': 'New Cases', 'recovered': 'Recovered',
        'tested': 'Tested', 'died': 'Died'
    })

    return dataFrame