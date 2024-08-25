from components.widgets.base import Widget
from dash import dcc, html
import dash_bootstrap_components as dbc

class FilterBoxWidget(Widget):
    def __init__(self, widget_info, cols, datapath):
        super().__init__(widget_info, cols, datapath)
        self.filter_types = widget_info.get('filterTypes', [])

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
            components.append(f"""
                html.Div([
                    dcc.DatePickerRange(
                        id='{self.name}_date_picker',
                        start_date=df['sepal_length'].min(),
                        end_date=df['sepal_length'].max(),
                        display_format='YYYY-MM-DD',
                        style={{
                            'backgroundColor': '#32383e',
                            'color': '#ffffff',
                            'border': '1px solid #4a4a4a',
                            'borderRadius': '5px',
                            'width': '100%'
                        }}
                    )
                ], style={{'marginBottom': '20px'}})
            """)

        if "Category" in self.filter_types:
            components.append(f"""
                html.Div([
                    dcc.Dropdown(
                        id='{self.name}_category_dropdown',
                        options=[
                            {{'label': 'Setosa', 'value': 'setosa'}},
                            {{'label': 'Versicolor', 'value': 'versicolor'}},
                            {{'label': 'Virginica', 'value': 'virginica'}}
                        ],
                        multi=True,
                        style={{
                            'backgroundColor': '#32383e',
                            'color': '#000000',
                            'border': '1px solid #4a4a4a',
                            'borderRadius': '5px',
                            'width': '100%'
                        }}
                    )
                ], style={{'marginBottom': '20px', 'backgroundColor': '#32383e', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)'}})
            """)

        if "Numeric Range" in self.filter_types:
            components.append(f"""
                html.Div([
                    dcc.RangeSlider(
                        id='{self.name}_numeric_slider',
                        min=df['sepal_length'].min(),
                        max=df['sepal_length'].max(),
                        step=0.1,
                        marks={{i: str(i) for i in range(int(df['sepal_length'].min()), int(df['sepal_length'].max())+1)}},
                        value=[df['sepal_length'].min(), df['sepal_length'].max()],
                        tooltip={{'always_visible': True, 'placement': 'bottom'}}
                    )
                ], style={{'marginBottom': '20px', 'backgroundColor': '#32383e', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)'}})
            """)

        return "html.Div([\n" + ",\n".join(components) + "\n])"

