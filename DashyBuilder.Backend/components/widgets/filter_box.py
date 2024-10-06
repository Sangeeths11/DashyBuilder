from components.widgets.base import Widget
from dash import dcc, html
import dash_bootstrap_components as dbc

from components.widgets.filter_types.date_range_filter import generate_date_range_filter_code
from components.widgets.filter_types.category_filter import generate_category_filter_code
from components.widgets.filter_types.numeric_range_filter import generate_numeric_range_filter_code

class FilterBoxWidget(Widget):
    def __init__(self, widget_info, cols, datapath):
        super().__init__(widget_info, cols, datapath)
        self.filter_types = widget_info.get('filterTypes', [])
        self.filterconfig = widget_info.get('filterConfig', {})

    def generate_code(self):
        self.title = self.name
        self.name = self.name.replace(" ", "")
        
        filter_components_code = self._generate_filter_components_code()

        return f"""
def drawFilterBox_{self.name}():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Label('{self.title}:', style={{'color': 'white'}}),
                {filter_components_code}
            ]), style={{'height': '100%'}}
        )
    ], style={{'height': '100%', 'padding': '2px'}})
"""

    def _generate_filter_components_code(self):
        components = []
        
        if "Date Range" in self.filter_types:
            components.append(generate_date_range_filter_code(self.name,self.filterconfig))

        if "Category" in self.filter_types:
            components.append(generate_category_filter_code(self.name))

        if "Numeric Range" in self.filter_types:
            components.append(generate_numeric_range_filter_code(self.name,self.filterconfig))

        return "html.Div([\n" + ",\n".join(components) + "\n])"

