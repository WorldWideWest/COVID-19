from dash import dcc, html, Input, Output
from datetime import datetime
import plotly.graph_objects as go

class Components(object):

    def date_picker(self, startDate:object, endDate:object, id = "date-picker-range") -> object:
        return dcc.DatePickerRange(
            id = id,
            start_date = startDate,
            end_date = endDate,
            initial_visible_month = endDate,
            display_format = "D.M.Y",
        )
        
    
    def dropdown(self, objects:list, default:int, id = "dropdown") -> list:
        options = [{"label":str(option), "value": option} for option in objects]
        return dcc.Dropdown(
            id = id,
            options = options,
            value = options[default]["value"]
        )


class Charts(object):
    def donut_char(self, dataFrame:object, dependent:str, independent:str, title:str, startDate = None, endDate = None) -> dict:
        # Date formating 
        startDate = datetime.strptime(startDate, "%Y-%m-%d")
        endDate = datetime.strptime(endDate, "%Y-%m-%d")

        filtered = dataFrame[(dataFrame.index >= startDate) & (dataFrame.index <= endDate)]

        # Filtering
        values = [filtered[[independent]].mean()[0] / filtered[[dependent]].mean()[0]]
        procentage = round((values[0] / values[1]) * 100, 2)
        labels = [str(dependent), str(independent)]

        data = [go.Pie(
            labels = labels, values = values, hole = .5
        )]

        layout = go.Layout(
            title = str(title),
        )

        return dict(data = data, layout = layout)


DROPDOWN_STYLE = {
    "width": "33%"
}

CONTAINER_ROW_STYLE = {
    "display": "flex",
    "flex-direction": "column",
    "justify-content": "space-evenlyee",
}




