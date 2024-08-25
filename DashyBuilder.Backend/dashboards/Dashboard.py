from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
df = px.data.iris()
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


def drawBubble_SDAS():
    
    fig = px.scatter(df, x='sepal_length', y='sepal_width', size='petal_length', color='species').update_layout(
        title={'text': 'SDAS', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
            
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    id='SDAS_graph',
                    figure=fig,
                    config={'displayModeBar': False},
                    style={'height': '100%', 'width': '100%'},
                    responsive=True
                )
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})


def drawBar_asd():
    
    fig = px.bar(df, x='species', y='sepal_length').update_layout(
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


def drawFilterBox_sad():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Label('sad:', style={'color': 'white'}),
                html.Div([

                html.Div([
                    dcc.Dropdown(
                        id='sad_category_dropdown',
                        options=[
                            {'label': 'Setosa', 'value': 'setosa'},
                            {'label': 'Versicolor', 'value': 'versicolor'},
                            {'label': 'Virginica', 'value': 'virginica'}
                        ],
                        multi=True,
                        style={
                            'backgroundColor': '#32383e',
                            'color': '#000000',
                            'border': '1px solid #4a4a4a',
                            'borderRadius': '5px',
                            'width': '100%'
                        }
                    )
                ], style={'marginBottom': '20px', 'backgroundColor': '#32383e', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)'})
            ,

                html.Div([
                    dcc.RangeSlider(
                        id='sad_numeric_slider',
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

app.layout = html.Div([
    dbc.Container([
        html.Div(style={
            'display': 'grid',
           'gridTemplateColumns': 'repeat(18, 1fr)',
           'gridTemplateRows': 'repeat(18, 1fr)',
            'gap': '10px',
            'height': '99vh'
        }, children=[
            html.Div(drawBubble_SDAS(), style={'gridColumn': '1 / span 15', 'gridRow': '11 / span 8', 'padding': '0px'}),
            html.Div(drawBar_asd(), style={'gridColumn': '1 / span 15', 'gridRow': '6 / span 5', 'padding': '0px'}),
            html.Div(drawFilterBox_sad(), style={'gridColumn': '16 / span 3', 'gridRow': '6 / span 5', 'padding': '0px'}),
        ])
    ], fluid=True, style={'height': '100vh', 'padding': '0', 'margin': '0', 'width': '100vw', 'overflow': 'hidden'})
])
if __name__ == '__main__':
    app.run_server(debug=True)