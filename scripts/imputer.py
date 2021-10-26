import pandas as pd
import json
import requests as re

def job():
    path = "../dataSet/cleanData.xlsx"
    url = "http://127.0.0.1:8000/api/"

    data = pd.read_excel(path, engine = "openpyxl")

    data['date'] = pd.to_datetime(data['date'], format = "%d.%m.%Y")
    data['date'] = data['date'].dt.strftime('%Y-%m-%d')

    result = data.to_json(orient="records")
    parsed = json.loads(result)
    jsonData = json.dumps(parsed, indent=4)

    headers = {
        'Content-type':'application/json', 
        'Accept':'application/json'
    }

    delete = re.delete(url)

    post = re.post(url, data = jsonData, headers = headers)
    print(post.status_code)

job()
