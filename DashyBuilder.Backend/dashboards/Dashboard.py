from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
df = px.data.iris()
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


def drawLine_asd():
    
    fig = px.line(df, x='sepal_length', y='sepal_width').update_layout(
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


def drawFilterBox_asd():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Label('asd:', style={'color': 'white'}),
                html.Div([

    html.Div([
        dcc.DatePickerRange(
            id='asd_date_picker',
            start_date='2023-08-27',
            end_date='2024-08-26',
            display_format='YYYY-MM-DD',
            style={
                'backgroundColor': '#32383e',
                'color': '#ffffff',
                'border': '1px solid #4a4a4a',
                'borderRadius': '5px',
                'width': '100%'
            }
        )
    ], style={'marginBottom': '20px'})
    ,

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

app.layout = html.Div([
    dbc.Container([
        html.Div(style={
            'display': 'grid',
           'gridTemplateColumns': 'repeat(18, 1fr)',
           'gridTemplateRows': 'repeat(18, 1fr)',
            'gap': '10px',
            'height': '99vh'
        }, children=[
            html.Div(drawLine_asd(), style={'gridColumn': '1 / span 15', 'gridRow': '1 / span 5', 'padding': '0px'}),
            html.Div(drawBar_asd(), style={'gridColumn': '1 / span 15', 'gridRow': '6 / span 5', 'padding': '0px'}),
            html.Div(drawBubble_SDAS(), style={'gridColumn': '1 / span 15', 'gridRow': '11 / span 8', 'padding': '0px'}),
            html.Div(drawFilterBox_asd(), style={'gridColumn': '16 / span 3', 'gridRow': '11 / span 8', 'padding': '0px'}),
        ])
    ], fluid=True, style={'height': '100vh', 'padding': '0', 'margin': '0', 'width': '100vw', 'overflow': 'hidden'})
])
if __name__ == '__main__':
    app.run_server(debug=True)