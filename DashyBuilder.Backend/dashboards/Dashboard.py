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


def drawChart_fasdf():
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
                    id='fasdf_graph',
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
            html.Div(drawChart_fasdf(), style={'gridColumn': '1 / span 2', 'gridRow': '1 / span 6', 'padding': '0px'}),
        ])
    ], fluid=True, style={'height': '100vh', 'padding': '0', 'margin': '0', 'width': '100vw', 'overflow': 'hidden'})
])
if __name__ == '__main__':
    app.run_server(debug=True)