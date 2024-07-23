from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Example table data
table_data = {
    'Spalte 1': [1, 2, 3, 4],
    'Spalte 2': ['A', 'B', 'C', 'D'],
    'Spalte 3': [10.1, 20.2, 30.3, 40.4]
}
table_df = pd.DataFrame(table_data)

# Load data
df = px.data.iris()

# Create a graph card
def drawFigure():
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
                    id='graph',
                    figure=fig,
                    config={'displayModeBar': False},
                    style={'height': '100%', 'width': '100%'},
                    responsive=True
                )
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})

# Create a table card
def drawTable():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    dbc.Table.from_dataframe(table_df, striped=True, bordered=True, hover=True, dark=True)
                ])
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})

# Create a text card
def drawText(text='Text'):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H4(text),
                ], style={'textAlign': 'center', 'color': 'white', 'height': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})

# Create a filter box
def drawFilterBox():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    dcc.Dropdown(
                        id='filter-dropdown',
                        options=[
                            {'label': 'Setosa', 'value': 'setosa'},
                            {'label': 'Versicolor', 'value': 'versicolor'},
                            {'label': 'Virginica', 'value': 'virginica'}
                        ],
                        value=['setosa', 'versicolor', 'virginica'],
                        multi=True,
                        style={'color': '#000'}
                    )
                ], style={'textAlign': 'center', 'padding': '10px'})
            ]), style={'height': '100%'}
        )
    ], style={'height': '100%', 'padding': '2px'})

# Initialize app with external stylesheets
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Define layout
app.layout = html.Div([
    dbc.Container([
        html.Div(style={
            'display': 'grid',
            'grid-template-columns': 'repeat(5, 1fr)',
            'grid-template-rows': 'repeat(5, 1fr)',
            'gap': '10px',
            'height': '99vh'
        }, children=[
            html.Div(drawFigure(), style={'grid-column': '1 / span 3', 'grid-row': '2 / span 2', 'padding': '0px'}),
            html.Div(drawFilterBox(), style={'grid-column': '4 / span 2', 'grid-row': '2 / span 2', 'padding': '0px'}),
            html.Div(drawTable(), style={'grid-column': '1 / span 5', 'grid-row': '4 / span 2', 'padding': '0px'}),
            html.Div(drawText(text='My first Dashboard'), style={'grid-column': '1 / span 2', 'grid-row': '1 / span 1', 'padding': '0px'}),
            html.Div(drawText(text='Made by Sangeeths'), style={'grid-column': '4 / span 2', 'grid-row': '1 / span 1', 'padding': '0px'}),
        ])
    ], fluid=True, style={'height': '100vh', 'padding': '0', 'margin': '0', 'width': '100vw', 'overflow': 'hidden'})
])

@app.callback(
    Output('graph', 'figure'),
    [Input('filter-dropdown', 'value')]
)
def update_graph(selected_values):
    filtered_df = df[df['species'].isin(selected_values)]
    fig = px.bar(
        filtered_df, x='sepal_width', y='sepal_length', color='species'
    ).update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)