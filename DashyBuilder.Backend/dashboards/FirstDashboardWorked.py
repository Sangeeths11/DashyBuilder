from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Beispiel-Tabellendaten
table_data = {
    'Spalte 1': [1, 2, 3, 4],
    'Spalte 2': ['A', 'B', 'C', 'D'],
    'Spalte 3': [10.1, 20.2, 30.3, 40.4]
}
table_df = pd.DataFrame(table_data)

# Daten laden
df = px.data.iris()

# Erstellt eine Graph-Card
def drawFigure():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x='sepal_width', y='sepal_length', color='species'
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor='rgba(0, 0, 0, 0)',
                        paper_bgcolor='rgba(0, 0, 0, 0)',
                        height=500,
                        margin=dict(l=20, r=20, t=20, b=20)
                    ),
                    config={
                        'displayModeBar': False
                    },
                    style={'height': '100%', 'width': '100%'}
                )
            ]),
            style={'height': '100%'}
        ),
    ], style={'height': '100%', 'padding': '2px'})

# Erstellt eine Table-Card
def drawTable():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    dbc.Table.from_dataframe(table_df, striped=True, bordered=True, hover=True, dark=True)
                ])
            ]),
            style={'height': '100%'}
        ),
    ], style={'height': '100%', 'padding': '2px'})

# App initialisieren mit externen Stylesheets
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Layout definieren
app.layout = html.Div([
    dbc.Container([
        # Define a CSS Grid container
        html.Div(style={
            'display': 'grid',
            'grid-template-columns': '1fr 1fr 1fr',
            'grid-template-rows': '1fr 1fr 1fr',
            'gap': '10px',
            'height': '99vh'
        }, children=[
            # First row (spanning two rows)
            html.Div(drawTable(), style={'grid-column': '1 / span 2', 'grid-row': '1 / span 2', 'padding': '0px'}),
            # Second row
            html.Div(drawFigure(), style={'grid-column': '3', 'grid-row': '1 / span 3', 'padding': '0px'}),
        ])
    ], fluid=True, style={'height': '100vh', 'padding': '0', 'margin': '0', 'width': '100vw', 'overflow': 'hidden'})
])

if __name__ == '__main__':
    app.run_server(debug=True)
