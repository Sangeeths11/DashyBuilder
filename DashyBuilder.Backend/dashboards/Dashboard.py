from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
df = px.data.iris()
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


def drawScatter_asd():
    
    fig = px.scatter(df, x='sepal_length', y='sepal_width', color='species').update_layout(
        title={'text': 'asd', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    id='asd_graph',
                    figure=fig,
                    config={'displayModeBar': False},
                    style={'height': '100%', 'width': '100%'},
                    responsive=True
                )
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})


def drawFilterBox_asd():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Label('asd:', style={'color': 'white'}),
                html.Div([

    html.Div([
        dcc.RangeSlider(
            id='asd_numeric_slider',
            min=df['sepal_length'].min(),
            max=df['sepal_length'].max(),
            step=0.1,
            marks={i: str(i) for i in range(int(df['sepal_length'].min()), int(df['sepal_length'].max())+1)},
            value=[df['sepal_length'].min(), df['sepal_length'].max()],
            tooltip={'always_visible': True, 'placement': 'bottom'}
        )
    ], style={'marginBottom': '20px', 'backgroundColor': '#32383e', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)'})
    
])
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})


def drawTextBlock_sad(text='sad'):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.H4(text, style={'textAlign': 'center', 'color': 'white', 'height': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})

app.layout = html.Div([
    dbc.Container([
        html.Div(style={
            'display': 'grid',
           'gridTemplateColumns': 'repeat(4, 1fr)',
           'gridTemplateRows': 'repeat(4, 1fr)',
            'gap': '10px',
            'height': '99vh'
        }, children=[
            html.Div(drawScatter_asd(), style={'gridColumn': '1 / span 4', 'gridRow': '3 / span 2', 'padding': '0px'}),
            html.Div(drawFilterBox_asd(), style={'gridColumn': '1 / span 4', 'gridRow': '2 / span 1', 'padding': '0px'}),
            html.Div(drawTextBlock_sad(), style={'gridColumn': '1 / span 4', 'gridRow': '1 / span 1', 'padding': '0px'}),
        ])
    ], fluid=True, style={'height': '100vh', 'padding': '0', 'margin': '0', 'width': '100vw', 'overflow': 'hidden'})
])
if __name__ == '__main__':
    app.run_server(debug=True)