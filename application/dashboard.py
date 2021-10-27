import dash
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output

import pandas as pd
from scipy.stats import linregress

from datetime import datetime

from functions.custom import get_data
from components import Components
from components import DROPDOWN_STYLE, CONTAINER_ROW_STYLE
from assets.colorscale import OrRd, Tableau10

component = Components()

app = dash.Dash(__name__)

dataFrame = pd.DataFrame(get_data("http://127.0.0.1:8000/api"))
dataFrame.set_index("Date", inplace = True)

# Layout

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
            component.dropdown(dataFrame.columns, 4, id = "dropdown-x-axis"),
        ]),
        
        # Y Axis
        html.Div(id = "y-axis-selector", children = [
            html.Label("Y Axis selector"),
            component.dropdown(dataFrame.columns, 1, id = "dropdown-y-axis"),
        ])
    ]),

    dcc.Tabs(id="tabs", value='tabs', children=[
        dcc.Tab(
            label='Descriptive statistics', value='tab-one', 
            children = [
                html.Div(id = "descriptive-stat", className = "flex-row", children = [
                        dcc.Graph(id = "infected-rate", style = {"width": "25%"}),
                        dcc.Graph(id = "death-rate", style = {"width": "25%"}),
                        dcc.Graph(id = "suffer-rate", style = {"width": "25%"}),
                        dcc.Graph(id = "tested-rate", style = {"width": "25%"}),
                ]),
                html.Div(id = "pandemic", className = "flex-row", children = [
                    dcc.Graph(id = "pandemic-overview", style = {"width": "100%"}),
                ])
            ]
        ),
        dcc.Tab(
            label='Correlation analysis', value='tab-two',
            children = [
                html.Div(id = "correlation-analysis", className = "flex-row", children = [
                    dcc.Graph(id = "heat-map", style = {"width": "40%"}),
                    dcc.Graph(id = "scatter-plot", style = {"width": "60%"}),
                ]),
            ]
        ),
        dcc.Tab(
            label='Regression analysis', value='tab-three',
            children = [
                html.Div(id = "regression-analysis", children = [
                    # dcc.Graph(id = "heat-map", style = {"width": "40%"}),
                    # dcc.Graph(id = "scatter-plot", style = {"width": "60%"}),
                ]),
            ]
        ),
    ]),

])


# Logic

# Descriptive statistics
@app.callback(
    Output("infected-rate", "figure"),
    [
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
    ])
def donut_char(startDate:str, endDate:str) -> dict:
    # Date formating 
    startDate = datetime.strptime(startDate, "%Y-%m-%d")
    endDate = datetime.strptime(endDate, "%Y-%m-%d")

    filtered = dataFrame[(dataFrame.index >= startDate) & (dataFrame.index <= endDate)]

    # Filtering
    values = [filtered[["New Cases"]].mean()[0], filtered[["Tested"]].mean()[0]]
    procentage = round((values[0] / values[1]) * 100, 2)
    labels = ["New Cases", "Tested"]

    data = [go.Pie(
        labels = labels, values = values, hole = .8, marker = {"colors": [OrRd[-1], OrRd[0]]}
    )]

    layout = go.Layout(
        title = f"Average procentage of <span style='color:{ OrRd[-1] }'>tested</span><br> people who are <span style = 'color: { OrRd[0] }'>infected</span>",
        font = {"size": 12},
        showlegend = False,
        paper_bgcolor = 'rgb(255, 255, 255, .65)',
        # plot_bgcolor = ''
    )

    return dict(data = data, layout = layout)

@app.callback(
    Output("death-rate", "figure"),
    [
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
    ]
)
def donut_char(startDate:str, endDate:str) -> dict:
    # Date formating 
    startDate = datetime.strptime(startDate, "%Y-%m-%d")
    endDate = datetime.strptime(endDate, "%Y-%m-%d")

    filtered = dataFrame[(dataFrame.index >= startDate) & (dataFrame.index <= endDate)]

    # Filtering
    values = [filtered[["New Cases"]].mean()[0], filtered[["Died"]].mean()[0]]
    procentage = round((values[0] / values[1]) * 100, 2)
    labels = ["New Cases", "Death"]

    data = [go.Pie(
        labels = labels, values = values, hole = .8, marker = {"colors": [OrRd[0], OrRd[-1]]}
    )]

    layout = go.Layout(
        title = f"Average procentage of <span style='color:{ OrRd[0] }'>infected</span><br>who <span style = 'color: { OrRd[-1] }'>died</span>",
        font = {"size": 12},
        showlegend = False,
        paper_bgcolor = 'rgb(255, 255, 255, .65)',
        # plot_bgcolor = ''
    )

    return dict(data = data, layout = layout)

@app.callback(
    Output("suffer-rate", "figure"),
    [
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
    ])
def donut_char(startDate:str, endDate:str) -> dict:
    # Date formating 
    startDate = datetime.strptime(startDate, "%Y-%m-%d")
    endDate = datetime.strptime(endDate, "%Y-%m-%d")

    filtered = dataFrame[(dataFrame.index >= startDate) & (dataFrame.index <= endDate)]
    suffered = filtered["New Cases"].sum()
    # Filtering
    values = [suffered, 3280000]
    print(values)
    procentage = round((values[0] / values[1]) * 100, 2)
    labels = ["Total Cases", "Total people"]

    data = [go.Pie(
        labels = labels, values = values, hole = .8, marker = {"colors": [OrRd[-1], OrRd[0]]}
    )]

    layout = go.Layout(
        title = f"Procentage of people<br>who <span style = 'color: { OrRd[-1] }'>suffered</span> from COVID in B&H",
        font = {"size": 12},
        showlegend = False,
        paper_bgcolor = 'rgb(255, 255, 255, .65)',
    )

    return dict(data = data, layout = layout)

@app.callback(
    Output("tested-rate", "figure"),
    [
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
    ])
def donut_char(startDate:str, endDate:str) -> dict:
    # Date formating 
    startDate = datetime.strptime(startDate, "%Y-%m-%d")
    endDate = datetime.strptime(endDate, "%Y-%m-%d")

    filtered = dataFrame[(dataFrame.index >= startDate) & (dataFrame.index <= endDate)]
    tested = filtered["Tested"].sum()
    # Filtering
    values = [tested, 3280000]
    print(values)
    procentage = round((values[0] / values[1]) * 100, 2)
    labels = ["Total Cases", "Total people"]

    data = [go.Pie(
        labels = labels, values = values, hole = .8, marker = {"colors": [OrRd[-1], OrRd[0]]}
    )]

    layout = go.Layout(
        title = f"Procentage of people<br>who are <span style = 'color: { OrRd[-1] }'>tested</span> on COVID in B&H",
        font = {"size": 12},
        showlegend = False,
        paper_bgcolor = 'rgb(255, 255, 255, .65)',
    )

    return dict(data = data, layout = layout)

@app.callback(
    Output("pandemic-overview", "figure"),
    [
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
    ])
def covid_time(startDate:str, endDate:str) -> dict:
    startDate = datetime.strptime(startDate, "%Y-%m-%d")
    endDate = datetime.strptime(endDate, "%Y-%m-%d")

    filtered = dataFrame[(dataFrame.index >= startDate) & (dataFrame.index <= endDate)]
    traceOne = go.Scatter(
        x = filtered.index, y = filtered["New Cases"], mode = "lines", name = "New Cases", line_color = Tableau10[0]
    )
    traceTwo = go.Scatter(
        x = filtered.index, y = filtered["Recovered"], mode = "lines", name = "Recovered", visible = "legendonly", line_color = Tableau10[1]
    )
    traceThree = go.Scatter(
        x = filtered.index, y = filtered["Tested"], mode = "lines", name = "Tested", line_color = Tableau10[2]
    )
    traceFour = go.Scatter(
        x = filtered.index, y = filtered["Died"], mode = "lines", name = "Died", visible = "legendonly", line_color = Tableau10[4]
    )

    data = [traceOne, traceTwo, traceThree, traceFour]

    layout = go.Layout(
        title = f"COVID - 19 pandemic in Bosnia and Herzegovina from { startDate.date().strftime('%b %d,%Y') } to { endDate.date().strftime('%b %d,%Y') }",
        font = {"size": 12},
        paper_bgcolor = 'rgb(255, 255, 255, .75)',
        plot_bgcolor = 'rgb(255, 255, 255, .75)'
    )

    return dict(data = data, layout = layout)




# Correlation 
@app.callback(
    Output("scatter-plot", "figure"),
    [
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
        Input("dropdown-x-axis", "value"),
        Input("dropdown-y-axis", "value"),
    ])
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
            "color": f"{ OrRd[0] }",
            "line": {"width": 1, "color": f"{ OrRd[-1] }"},
        },
        hovertemplate = f"{ xVals }: " + "%{x},<br>" + f"{ yVals }: " + "%{y}<br>",
        hoverinfo = None
    )]

    layout = go.Layout(
        title = f"Correlation of variables { xVals } and { yVals } between { startDate.date().strftime('%b %d,%Y') } to { endDate.date().strftime('%b %d,%Y') }",
        xaxis = {"title": str(xVals)},
        yaxis = {"title": str(yVals)}
    )

    return dict(data = data, layout = layout)

@app.callback(
    Output("heat-map", "figure"),
    [
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
    ])
def heatmap(startDate:str, endDate:str) -> dict:

    filtered = dataFrame[
        (dataFrame.index >= startDate) & (dataFrame.index <= endDate) 
    ]

    matrix = filtered.corr()

    data = [
        go.Heatmap(
            x = matrix.columns.values, y = matrix.columns.values, z = matrix.values,
            colorscale = OrRd, meta = {"text": True}
        )
    ]

    layout = go.Layout(
        title = "Correlation matrix between all variables for the selected period",
    )

    return dict(data = data, layout = layout)
















if __name__ == "__main__":
    app.run_server(debug = True, port = 8050)
