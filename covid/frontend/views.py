import pandas as pd
import requests

from django.shortcuts import render

# Create your views here.

def analysis_view(request):
    pd.set_option('colheader_justify', 'center') 
    pd.options.display.max_rows = 100
    url = "http://127.0.0.1:8000/api/"
    get = requests.get(url)

    # df = df.rename(columns={"Category":"Pet"})

    # Parsing the json data to dataFrame
    dataFrame = pd.read_json(get.content)
    dataFrame = dataFrame[['date', 'total_cases', 'new_cases', 'recovered', 'tested', 'died']]
    
    dataFrame = dataFrame.rename(columns = {
        'date': 'Date', 'total_cases': 'Total Cases', 
        'new_cases': 'New Cases', 'recovered': 'Recovered',
        'tested': 'Tested', 'died': 'Died'
    })



    dataFrame = dataFrame.to_html(
        col_space = 100, index = False, max_rows = 10,
        classes = (
            ('class', 'table table-hover')
        )
    )
    context = {
        "dataFrame": dataFrame,
    }

    return render(request, "analysis.html", context)

# def api_view(request):
#     context = {}
#     return render(request, "analysis.html", context)

def about_view(request):
    context = {}
    return render(request, "about.html", context)