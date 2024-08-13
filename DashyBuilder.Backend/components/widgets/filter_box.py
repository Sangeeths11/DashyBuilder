from components.widgets.base import Widget

class FilterBoxWidget(Widget):
    def generate_code(self):
        self.name = self.name.replace(" ", "")
        return f"""
def drawFilterBox_{self.name}():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Dropdown(
                    id='{self.name}_dropdown',
                    options=[{{'label': 'Setosa', 'value': 'setosa'}}, {{'label': 'Versicolor', 'value': 'versicolor'}}, {{'label': 'Virginica', 'value': 'virginica'}}],
                    value=['setosa', 'versicolor', 'virginica'],
                    multi=True,
                    style={{
                        'backgroundColor': '#32383e',  # Dropdown background color
                        'color': '#000',  # Text color
                        'border': '1px solid #4a4a4a',  # Border color
                        'borderRadius': '5px',  # Rounded corners
                        'padding': '5px',  # Inner padding
                        'fontFamily': 'Arial, sans-serif',  # Font style
                        'fontSize': '14px'  # Font size
                    }}
                )
            ]), style={{'height': '100%'}}
        )
    ], style={{'height': '100%', 'padding': '2px'}})
"""
