from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
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


def drawTextBlock_ProfitAnalysisSummary(text='Profit Analysis Summary'):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.H4(text, style={'textAlign': 'center', 'color': 'white', 'height': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})


def drawChart_ProfitbyCoffeeType():
    fig = px.pie(df, names='species', values='sepal_length').update_layout(
        title={'text': 'Profit by Coffee Type', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    id='ProfitbyCoffeeType_graph',
                    figure=fig,
                    config={'displayModeBar': False},
                    style={'height': '100%', 'width': '100%'},
                    responsive=True
                )
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})


def drawFilterBox_FilterbyCoffeeName():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Label('Filter by Coffee Name:', style={'color': 'white'}),
                html.Div([
                    html.Select(
                        id='FilterbyCoffeeName_select',
                        className='form-select',
                        children=[
                            html.Option('Setosa', value='setosa'),
                            html.Option('Versicolor', value='versicolor'),
                            html.Option('Virginica', value='virginica')
                        ],
                        style={
                            'backgroundColor': '#32383e',
                            'color': '#ffffff',
                            'border': '1px solid #4a4a4a',
                            'borderRadius': '5px',
                            'width': '100%'
                        }
                    )
                ], style={'padding': '10px', 'backgroundColor': '#32383e', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)'})
                ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})


def drawTable_CoffeeSalesOverview():
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
        title={'text': 'Coffee Sales Overview', 'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
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
                    id='CoffeeSalesOverview_graph',
                    figure=fig,
                    config={'displayModeBar': False},
                    style={'height': '100%', 'width': '100%'},
                    responsive=True
                )
            ]), style={'height': '100%', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)', 'borderRadius': '10px', 'backgroundColor': '#32383e'}
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
            html.Div(drawTextBlock_ProfitAnalysisSummary(), style={'gridColumn': '1 / span 6', 'gridRow': '1 / span 1', 'padding': '0px'}),
            html.Div(drawChart_ProfitbyCoffeeType(), style={'gridColumn': '1 / span 4', 'gridRow': '3 / span 2', 'padding': '0px'}),
            html.Div(drawFilterBox_FilterbyCoffeeName(), style={'gridColumn': '5 / span 2', 'gridRow': '3 / span 2', 'padding': '0px'}),
            html.Div(drawTable_CoffeeSalesOverview(), style={'gridColumn': '1 / span 6', 'gridRow': '5 / span 2', 'padding': '0px'}),
        ])
    ], fluid=True, style={'height': '100vh', 'padding': '0', 'margin': '0', 'width': '100vw', 'overflow': 'hidden'})
])
if __name__ == '__main__':
    app.run_server(debug=True)