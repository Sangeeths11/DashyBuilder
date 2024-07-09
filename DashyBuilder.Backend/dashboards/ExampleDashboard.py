from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

def drawFigure():
    df = px.data.iris()
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(df, x='sepal_width', y='sepal_length', color='species')
                        .update_layout(
                            template='plotly_dark',
                            plot_bgcolor='rgba(0, 0, 0, 0)',
                            paper_bgcolor='rgba(0, 0, 0, 0)',
                        ),
                    config={'displayModeBar': False}
                )
            ])
        ),
    ])

def drawText(content='Text'):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2(content),
                ], style={'textAlign': 'center'})
            ])
        ),
    ])

def drawTable():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Table([
                    html.Thead([
                        html.Tr([
                            html.Th('Column 1'),
                            html.Th('Column 2'),
                        ])
                    ]),
                    html.Tbody([
                        html.Tr([
                            html.Td('Value 1'),
                            html.Td('Value 2'),
                        ])
                    ])
                ])
            ])
        ),
    ])

app = Dash(external_stylesheets=[dbc.themes.SLATE])
app.layout = html.Div([
    dbc.Row([
        dbc.Col(drawText('Dashboard Title'), width=12),
    ], align='center'),
dbc.Col(drawFigure(), width=6),
dbc.Col(drawTable(), width=6),
])

if __name__ == '__main__':
    app.run_server(debug=True)