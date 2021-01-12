import os
import pandas as pd
import cufflinks as cf
import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from datetime import datetime as dt


class Process:
    def Import(fileName, path = "./dataSet/cleanData"):
        return pd.read_excel(os.path.join(path, str(fileName)), engine = "openpyxl")

    def SingleLinePlot(dataFrame, columns, title, labels, lineColor = "#001024"):
        fig = px.line(dataFrame, x = columns[0], y = columns[1], title = f"{title}")

        fig.update_traces(line_color = lineColor)
        fig.update_layout(xaxis_title = f"{labels[0]}", yaxis_title = f"{labels[1]}")
        
        return fig
