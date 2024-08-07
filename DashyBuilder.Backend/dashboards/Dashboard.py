from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
table_data = {
    'Spalte 1': [1, 2, 3, 4],
    'Spalte 2': ['A', 'B', 'C', 'D'],
    'Spalte 3': [10.1, 20.2, 30.3, 40.4]
}
table_df = pd.DataFrame(table_data)
df = px.data.iris()
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


def drawTextBlock_asd(text='Text'):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.H4(text, style={'textAlign': 'center', 'color': 'white', 'height': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})


def drawTextBlock_dasd(text='Text'):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.H4(text, style={'textAlign': 'center', 'color': 'white', 'height': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})


def drawTable_asda():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dbc.Table.from_dataframe(table_df, striped=True, bordered=True, hover=True, dark=True, responsive=True, style={'width': '100%', 'overflowY': 'auto'})
            ]), style={'height': '100%', 'overflow': 'hidden'}
        )
    ], style={'height': '100%', 'padding': '2px'})

app.layout = html.Div([
    dbc.Container([
        html.Div(style={
            'display': 'grid',
           'gridTemplateColumns': 'repeat(12, 1fr)',
           'gridTemplateRows': 'repeat(12, 1fr)',
            'gap': '10px',
            'height': '99vh'
        }, children=[
            html.Div(drawTextBlock_asd(), style={'gridColumn': '1 / span 1', 'gridRow': '1 / span 12', 'padding': '0px'}),
            html.Div(drawTextBlock_dasd(), style={'gridColumn': '3 / span 10', 'gridRow': '1 / span 7', 'padding': '0px'}),
            html.Div(drawTable_asda(), style={'gridColumn': '5 / span 4', 'gridRow': '10 / span 3', 'padding': '0px'}),
        ])
    ], fluid=True, style={'height': '100vh', 'padding': '0', 'margin': '0', 'width': '100vw', 'overflow': 'hidden'})
])
if __name__ == '__main__':
    app.run_server(debug=True)