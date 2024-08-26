from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
df = px.data.iris()
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

def drawFilterBox_asd():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Label('Filter by Sepal Length:', style={'color': 'white'}),
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
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})

def drawTable_asd():
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='#2e3338',
                    font=dict(color='white', size=14, family='Arial'),
                    align='center',
                    height=30),
                    
        cells=dict(values=[df[col] for col in df.columns],
                   fill_color=[['#3b4147', '#434a51']*len(df)],
                   align='center',
                   font=dict(color='white', size=12, family='Arial'),
                   height=25)
    )])

    fig.update_layout(
        title={'text': 'Iris Data Table', 'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
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
            ]), style={'height': '100%', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)', 'borderRadius': '10px', 'backgroundColor': '#32383e'}
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
                    id='asd_bar_graph',  # ID geändert, um den Callback zu ermöglichen
                    figure=fig,
                    config={'displayModeBar': False},
                    style={'height': '100%', 'width': '100%'},
                    responsive=True
                )
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})

def drawTextBlock_asda(text='Iris Dataset Visualization'):
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
           'gridTemplateColumns': 'repeat(12, 1fr)',
           'gridTemplateRows': 'repeat(12, 1fr)',
            'gap': '10px',
            'height': '99vh'
        }, children=[
            html.Div(drawFilterBox_asd(), style={'gridColumn': '1 / span 12', 'gridRow': '5 / span 1', 'padding': '0px'}),
            html.Div(drawTable_asd(), style={'gridColumn': '1 / span 12', 'gridRow': '9 / span 4', 'padding': '0px'}),
            html.Div(drawBar_asd(), style={'gridColumn': '1 / span 12', 'gridRow': '6 / span 3', 'padding': '0px'}),
            html.Div(drawTextBlock_asda(), style={'gridColumn': '1 / span 12', 'gridRow': '1 / span 1', 'padding': '0px'}),
        ])
    ], fluid=True, style={'height': '100vh', 'padding': '0', 'margin': '0', 'width': '100vw', 'overflow': 'hidden'})
])

@app.callback(
    Output('asd_bar_graph', 'figure'),
    Input('asd_numeric_slider', 'value')
)
def update_bar_chart(sepal_length_range):
    filtered_df = df[(df['sepal_length'] >= sepal_length_range[0]) & (df['sepal_length'] <= sepal_length_range[1])]
    fig = px.bar(filtered_df, x='species', y='sepal_length').update_layout(
        title={'text': 'Sepal Length per Species', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
