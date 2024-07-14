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
            dbc.Col(drawText("Block 1"), width=4),
            dbc.Col(drawText("Block 2"), width=4),
            dbc.Col([
                dbc.Row([drawText("Block 3A")], style={"height": "25%"}),
                dbc.Row([drawText("Block 3B")], style={"height": "25%"}),
                dbc.Row([drawText("Block 3C")], style={"height": "25%"}),
                dbc.Row([drawText("Block 3D")], style={"height": "25%"})
            ], width=4)
        ]),
        dbc.Row([
            dbc.Col(drawFigure(), width=4),
            dbc.Col(drawFigure(), width=4),
            dbc.Col([
                dbc.Row([drawText("Block 6A")], style={"height": "25%"}),
                dbc.Row([drawText("Block 6B")], style={"height": "25%"}),
                dbc.Row([drawText("Block 6C")], style={"height": "25%"}),
                dbc.Row([drawText("Block 6D")], style={"height": "25%"})
            ], width=4)
        ]),
        dbc.Row([
            dbc.Col(drawText("Block 7"), width=4),
            dbc.Col(drawText("Block 8"), width=4),
            dbc.Col([
                dbc.Row([drawText("Block 9A")], style={"height": "25%"}),
                dbc.Row([drawText("Block 9B")], style={"height": "25%"}),
                dbc.Row([drawText("Block 9C")], style={"height": "25%"}),
                dbc.Row([drawText("Block 9D")], style={"height": "25%"})
            ], width=4)
        ])
    ], fluid=True)
])

# Server starten
if __name__ == '__main__':
    app.run_server(debug=True)
