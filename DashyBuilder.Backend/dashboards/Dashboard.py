from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
df = pd.read_csv('C:\\Users\\csang\\.vscode\\DashyBuilder\\DashyBuilder.Backend\\dashboards\\Iris.xls')
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


def drawPie_pie():
    
    fig = px.pie(df, names='Species', values='SepalLengthCm').update_layout(
        title={'text': 'pie', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    id='pie_Pie_graph',
                    figure=fig,
                    config={'displayModeBar': False},
                    style={'height': '100%', 'width': '100%'},
                    responsive=True
                )
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})


def drawBar_BestSellingCoffee():
    
    fig = px.bar(df, x='SepalLengthCm', y='Species').update_layout(
        title={'text': 'Best Selling Coffee', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    id='BestSellingCoffee_Bar_graph',
                    figure=fig,
                    config={'displayModeBar': False},
                    style={'height': '100%', 'width': '100%'},
                    responsive=True
                )
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})


def drawBubble_bubble():
    
    fig = px.scatter(df, x='PetalLengthCm', y='PetalWidthCm', size='SepalLengthCm', color='Species').update_layout(
        title={'text': 'bubble', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    id='bubble_Bubble_graph',
                    figure=fig,
                    config={'displayModeBar': False},
                    style={'height': '100%', 'width': '100%'},
                    responsive=True
                )
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})


def drawScatter_asd():
    
    fig = px.scatter(df, x='SepalLengthCm', y='SepalWidthCm', color='Species').update_layout(
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
                    id='asd_Scatter_graph',
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
           'gridTemplateColumns': 'repeat(6, 1fr)',
           'gridTemplateRows': 'repeat(6, 1fr)',
            'gap': '10px',
            'height': '99vh'
        }, children=[
            html.Div(drawPie_pie(), style={'gridColumn': '4 / span 3', 'gridRow': '1 / span 2', 'padding': '0px'}),
            html.Div(drawBar_BestSellingCoffee(), style={'gridColumn': '1 / span 6', 'gridRow': '5 / span 2', 'padding': '0px'}),
            html.Div(drawBubble_bubble(), style={'gridColumn': '1 / span 6', 'gridRow': '3 / span 2', 'padding': '0px'}),
            html.Div(drawScatter_asd(), style={'gridColumn': '1 / span 3', 'gridRow': '1 / span 2', 'padding': '0px'}),
        ])
    ], fluid=True, style={'height': '100vh', 'padding': '0', 'margin': '0', 'width': '100vw', 'overflow': 'hidden'})
])
@app.callback(
    Output('asd_graph', 'figure'),
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