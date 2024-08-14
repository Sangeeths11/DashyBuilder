from components.widgets.base import Widget

class FilterBoxWidget(Widget):
    def generate_code(self):
        self.title = self.name
        self.name = self.name.replace(" ", "")
        return f"""
def drawFilterBox_{self.name}():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Label('{self.title}:', style={{'color': 'white'}}),
                html.Div([
                    html.Select(
                        id='{self.name}_select',
                        className='form-select',
                        children=[
                            html.Option('Setosa', value='setosa'),
                            html.Option('Versicolor', value='versicolor'),
                            html.Option('Virginica', value='virginica')
                        ],
                        style={{
                            'backgroundColor': '#32383e',
                            'color': '#ffffff',
                            'border': '1px solid #4a4a4a',
                            'borderRadius': '5px',
                            'padding': '
                            'width': '100%'
                        }}
                    )
                ], style={{'padding': '10px', 'backgroundColor': '#32383e', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)'}})
                ]), style={{'height': '100%'}}
        )
    ], style={{'height': '100%', 'padding': '2px'}})
"""
