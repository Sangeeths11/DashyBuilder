from components.widgets.base import Widget

class FilterBoxWidget(Widget):
    def generate_code(self):
        self.name = self.name.replace(" ", "")
        return f"""
def drawFilterBox_{self.name}():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Label('Filter by {self.name}:', style={{'color': 'white'}}),
                html.Div([
                    html.Select(
                        id='{self.name}_select',
                        className='form-select',  # Bootstrap class for styling the select element
                        children=[
                            html.Option('Setosa', value='setosa'),
                            html.Option('Versicolor', value='versicolor'),
                            html.Option('Virginica', value='virginica')
                        ],
                        style={{
                            'backgroundColor': '#32383e',  # Custom background color
                            'color': '#ffffff',  # Custom text color
                            'border': '1px solid #4a4a4a',  # Custom border color
                            'borderRadius': '5px',  # Rounded corners
                            'padding': '5px',  # Padding inside the select box
                            'width': '100%'  # Make sure it takes full width of the container
                        }}
                    )
                ], style={{'padding': '10px', 'backgroundColor': '#32383e', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)'}})
                ]), style={{'height': '100%'}}
        )
    ], style={{'height': '100%', 'padding': '2px'}})
"""
