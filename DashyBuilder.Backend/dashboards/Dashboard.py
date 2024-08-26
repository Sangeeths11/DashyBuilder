from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
df = px.data.iris()
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


def drawTextBlock_weq(text='weq'):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.H4(text, style={'textAlign': 'center', 'color': 'white', 'height': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})


def drawLine_ads():
    
    fig = px.line(df, x='sepal_length', y='sepal_width').update_layout(
        title={'text': 'ads', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    id='ads_graph',
                    figure=fig,
                    config={'displayModeBar': False},
                    style={'height': '100%', 'width': '100%'},
                    responsive=True
                )
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})

app.layout = html.Div([
    dbc.Container([
        html.Div(style={
            'display': 'grid',
           'gridTemplateColumns': 'repeat(3, 1fr)',
           'gridTemplateRows': 'repeat(3, 1fr)',
            'gap': '10px',
            'height': '99vh'
        }, children=[
            html.Div(drawTextBlock_weq(), style={'gridColumn': '1 / span 3', 'gridRow': '1 / span 1', 'padding': '0px'}),
            html.Div(drawLine_ads(), style={'gridColumn': '1 / span 3', 'gridRow': '2 / span 2', 'padding': '0px'}),
        ])
    ], fluid=True, style={'height': '100vh', 'padding': '0', 'margin': '0', 'width': '100vw', 'overflow': 'hidden'})
])
if __name__ == '__main__':
    app.run_server(debug=True)