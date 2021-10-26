import dash
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output

from datetime import datetime

from functions.custom import get_data
from components import Components
from components import DROPDOWN_STYLE, CONTAINER_ROW_STYLE
from assets.colorscale import OrRd

component = Components()

app = dash.Dash(__name__)

dataFrame = pd.DataFrame(get_data("http://127.0.0.1:8000/api"))
dataFrame
dataFrame.set_index("Date", inplace = True)


app.layout = html.Div(id = "app-body", children = [

    # Properties picker
    html.Div(id = "properties-panel", children = [
        html.Div(id = "date-picker", children = [
            html.Label("Pick the period"),
            component.date_picker(dataFrame.index.date.min(), dataFrame.index.date.max()),
        ], style = CONTAINER_ROW_STYLE),
        
        # X Axis
        html.Div(id = "x-axis-selector", children = [
            html.Label("X Axis selector"),
            component.dropdown(dataFrame.columns, 3, id = "dropdown-x-axis"),
        ]),
        
        # Y Axis
        html.Div(id = "y-axis-selector", children = [
            html.Label("Y Axis selector"),
            component.dropdown(dataFrame.columns, 1, id = "dropdown-y-axis"),
        ])
    ]),

    html.Div(id = "correlation-analysis", children = [
        dcc.Graph(id = "heat-map", style = {"width": "40%"}),
        dcc.Graph(id = "scatter-plot", style = {"width": "60%"})
    ])
])




@app.callback(
    Output("scatter-plot", "figure"),
    [
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
        Input("dropdown-x-axis", "value"),
        Input("dropdown-y-axis", "value"),
    ]
)
def scatter_plot(startDate:str, endDate:str,  xVals:str, yVals:str) -> dict:
    startDate = datetime.strptime(startDate, "%Y-%m-%d")
    endDate = datetime.strptime(endDate, "%Y-%m-%d")
    
    filtered = dataFrame[
        (dataFrame.index >= startDate) & (dataFrame.index <= endDate) 
    ]

    data = [go.Scatter(
        x = filtered[xVals], y = filtered[yVals], 
        mode = "markers", 
        opacity = .8,
        marker = {
            "size": 8,
            "color": f"{ OrRd[-1] }",
            "line": {"width": 1, "color": "#446DF6"},
        },        
    )]

    layout = go.Layout(
        title = f"Correlation between { xVals } and { yVals }",
        xaxis = {"title": str(xVals)},
        yaxis = {"title": str(yVals)}
    )

    return dict(data = data, layout = layout)

@app.callback(
    Output("heat-map", "figure"),
    [
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
    ]
)
def heat_map(startDate:str, endDate:str) -> dict:

    filtered = dataFrame[
        (dataFrame.index >= startDate) & (dataFrame.index <= endDate) 
    ]

    matrix = filtered.corr()

    data = [
        go.Heatmap(
            x = matrix.columns.values, y = matrix.columns.values, z = matrix.values,
            colorscale = OrRd,
        )
    ]

    layout = go.Layout(
        title = "Correlation matrix between all variables for the selected period",
    )

    return dict(data = data, layout = layout)

if __name__ == "__main__":
    app.run_server(debug = True, port = 8050)
