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


def drawTable_StudentAcademicPerformanceOverview():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dbc.Table.from_dataframe(table_df, striped=True, bordered=True, hover=True, dark=True, responsive=True, style={'width': '100%', 'overflowY': 'auto'})
            ]), style={'height': '100%', 'overflow': 'hidden'}
        )
    ], style={'height': '100%', 'padding': '2px'})


def drawChart_ParentalSupportvsGPA():
    fig = px.bar(df, x='sepal_width', y='sepal_length', color='species').update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    id='ParentalSupportvsGPA_graph',
                    figure=fig,
                    config={'displayModeBar': False},
                    style={'height': '100%', 'width': '100%'},
                    responsive=True
                )
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})


def drawChart_GPAvsExtracurricularActivities():
    fig = px.bar(df, x='sepal_width', y='sepal_length', color='species').update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    id='GPAvsExtracurricularActivities_graph',
                    figure=fig,
                    config={'displayModeBar': False},
                    style={'height': '100%', 'width': '100%'},
                    responsive=True
                )
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})


def drawTextBlock_AnalysisofExtracurricularActivitiesandParentalSupport(text='Text'):
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
           'gridTemplateColumns': 'repeat(5, 1fr)',
           'gridTemplateRows': 'repeat(5, 1fr)',
            'gap': '10px',
            'height': '99vh'
        }, children=[
            html.Div(drawTable_StudentAcademicPerformanceOverview(), style={'gridColumn': '1 / span 5', 'gridRow': '2 / span 2', 'padding': '0px'}),
            html.Div(drawChart_ParentalSupportvsGPA(), style={'gridColumn': '1 / span 2', 'gridRow': '4 / span 2', 'padding': '0px'}),
            html.Div(drawChart_GPAvsExtracurricularActivities(), style={'gridColumn': '4 / span 2', 'gridRow': '4 / span 2', 'padding': '0px'}),
            html.Div(drawTextBlock_AnalysisofExtracurricularActivitiesandParentalSupport(), style={'gridColumn': '1 / span 5', 'gridRow': '1 / span 1', 'padding': '0px'}),
        ])
    ], fluid=True, style={'height': '100vh', 'padding': '0', 'margin': '0', 'width': '100vw', 'overflow': 'hidden'})
])
if __name__ == '__main__':
    app.run_server(debug=True)