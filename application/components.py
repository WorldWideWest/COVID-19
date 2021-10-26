from dash import dcc, html, Input, Output



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



DROPDOWN_STYLE = {
    "width": "33%"
}

CONTAINER_ROW_STYLE = {
    "display": "flex",
    "flex-direction": "column",
    "justify-content": "space-evenlyee",
}




