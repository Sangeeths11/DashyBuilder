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
                        height=250,  # Höhe des Diagramms anpassen
                        margin=dict(l=20, r=20, t=20, b=20)  # Ränder des Diagramms anpassen
                    ),
                    config={
                        'displayModeBar': False
                    },
                    style={'height': '100%', 'width': '100%'}  # Stil der Komponente anpassen
                )
            ]),
            style={"height": "100%"}  # Stelle sicher, dass alle Karten gleich hoch sind
        ),
    ], style={"height": "100%", "padding": "2px"})  # Reduziere Padding, um Platz zu sparen

# App initialisieren mit externen Stylesheets
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Layout definieren
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(drawFigure(), width=4, style={"padding": "0px"}),  # Padding entfernt
            dbc.Col(drawFigure(), width=4, style={"padding": "0px"}),  # Padding entfernt
            dbc.Col(drawFigure(), width=4, style={"padding": "0px"}),  # Padding entfernt
        ], style={"height": "33vh", "margin": "0px"}),  # Höhe der Zeile und Margin angepasst
        dbc.Row([
            dbc.Col(drawFigure(), width=4, style={"padding": "0px"}),  # Padding entfernt
            dbc.Col(drawFigure(), width=4, style={"padding": "0px"}),  # Padding entfernt
            dbc.Col(drawFigure(), width=4, style={"padding": "0px"}),  # Padding entfernt
        ], style={"height": "33vh", "margin": "0px"}),  # Höhe der Zeile und Margin angepasst
        dbc.Row([
            dbc.Col(drawFigure(), width=4, style={"padding": "0px"}),  # Padding entfernt
            dbc.Col(drawFigure(), width=4, style={"padding": "0px"}),  # Padding entfernt
            dbc.Col(drawFigure(), width=4, style={"padding": "0px"}),  # Padding entfernt
        ], style={"height": "33vh", "margin": "0px"}),  # Höhe der Zeile und Margin angepasst
    ], fluid=True, style={"height": "100vh", "padding": "0", "margin": "0", "width": "100vw", "overflow": "hidden"})  # Stellt sicher, dass der Container die volle Bildschirmbreite einnimmt und kein zusätzliches Padding hat
])

# Server starten
if __name__ == '__main__':
    app.run_server(debug=True)
