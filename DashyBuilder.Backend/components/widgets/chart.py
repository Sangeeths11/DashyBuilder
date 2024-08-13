from components.widgets.base import Widget

class ChartWidget(Widget):
    def generate_code(self):
        self.title = self.name
        self.name = self.name.replace(" ", "")
        return f"""
def drawChart_{self.name}():
    fig = px.pie(df, names='species', values='sepal_length').update_layout(
        title={{'text': '{self.title}', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'}},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    id='{self.name}_graph',
                    figure=fig,
                    config={{'displayModeBar': False}},
                    style={{'height': '100%', 'width': '100%'}},
                    responsive=True
                )
            ]), style={{'height': '100%'}}
        )
    ], style={{'height': '100%', 'padding': '2px'}})
"""