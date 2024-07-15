from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

# Daten laden
df = px.data.iris()

# Erstellt eine Graph-Card
def drawFigure():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor='rgba(0, 0, 0, 0)',
                        paper_bgcolor='rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                )
            ]),
            style={"height": "100%"}  # Stelle sicher, dass alle Karten gleich hoch sind
        ),
    ])

# Erstellt eine Text-Card
def drawText(text="Text"):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H4(text),
                ], style={'textAlign': 'center'})
            ]),
            style={"height": "100%"}  # Gleiches Höheneinstellung wie bei den Graphen
        ),
    ])

# App initialisieren mit externen Stylesheets
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Layout definieren
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(drawFigure(), width=4),
            dbc.Col(dbc.Row([
                dbc.Col(drawFigure(), width=6),
                dbc.Col(drawFigure(), width=6),
            ]), width=4),
            
        ]),
        dbc.Row([
            dbc.Col(drawFigure(), width=4),
            dbc.Col(drawFigure(), width=4),
            dbc.Col(drawFigure(), width=4),
        ]),
        dbc.Row([
            dbc.Col(drawFigure(), width=4),
            dbc.Col(drawFigure(), width=4),
            dbc.Col(drawFigure(), width=4),
        ])
    ], fluid=True, style={"height": "100vh"})  # Stellt sicher, dass der Container die volle Bildschirmhöhe einnimmt
])

# Server starten
if __name__ == '__main__':
    app.run_server(debug=True)
