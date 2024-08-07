from components.widgets.base import Widget

class ChartWidget(Widget):
    def generate_code(self):
        self.name = self.name.replace(" ", "")
        return f"""
def drawChart_{self.name}():
    fig = px.bar(df, x='sepal_width', y='sepal_length', color='species').update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=20, b=20)
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
