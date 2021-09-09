from django.shortcuts import render

import json
import pandas as pd

from .customs import getDataFrame
# Create your views here.

def analysis_view(request):
    dataFrame = getDataFrame()

    corrFrame = dataFrame.corr().to_html(
        max_rows = 10,
        classes = (
            ('class', 'table table-hover custom')
        )
    )

    dataFrame = dataFrame.to_html(
        col_space = 100, index = False, max_rows = 10,
        classes = (
            ('class', 'table table-hover')
        )
    )

    context = {
        "dataFrame": dataFrame,
        "corrFrame": corrFrame,
    }

    return render(request, "analysis.html", context)


def about_view(request):
    context = {}
    return render(request, "about.html", context)





# Correlation matrix in d3.js
# data - consists of 6 columns
# calculate the correlation for each column in the axis (x, y)
#               Date     Total Cases     New Cases    Recovered    Tested     Died
# Date            1
# Total Cases               1
# New Cases                                 1
# Recovered                                                1
# Tested                                                              1
# Died                                                                          1
#                       PART 1             |                PART 2
# Formula rxy = sum((xi - Xbar)(yi - Ybar))/sqrt((xi - Xbar)^2(yi - Ybar)^2)
# Example Tested & New Cases
# xArray = Tested yArray = New Cases
#       Xbar = average(x)
#       Xbar = average(y)
#       SUM, SQRT, rxy = 0, 0, 0
#
# forEach i in (xArray, yArray):
#   xVal = xArray[i] - Xbar
#   yVal = yArray[i] - Ybar
#   
#   // PART 1
#   SUM += sum(xVal * yVal)
#   
#   // PART 2
#   SQRT += sqrt(xVal^2 * yVal^2)
#
#   if lenght of arrays(x, y) == i:
#       rxy = SUM / SQRT
#   
#   // DAta structure
#   json = {
#    "tested":{
#           "date": -.32,
#           "total_cases": .3
#           "new_cases": .3
#           "recovered": .4
#           "tested": 1
#           "died": .1
#       }
#    "died":{
#           "date": -.32,
#           "total_cases": .3
#           "new_cases": .3
#           "recovered": .4
#           "tested": 1
#           "died": .1
#       }....
#   }
#  
#
#