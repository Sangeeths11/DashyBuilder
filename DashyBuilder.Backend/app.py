from flask import Flask, request, make_response
from flask_cors import CORS
import json
from components.plotly_chart import PlotlyChart
from components.plotly_text_block import PlotlyTextBlock
from components.plotly_table import PlotlyTable

app = Flask(__name__)
CORS(app, expose_headers=['Content-Disposition'])

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h1>'

def generate_plotly_code(widgets):
    code_lines = [
        "from dash import Dash, dcc, html",
        "import dash_bootstrap_components as dbc",
        "import plotly.express as px",
        "",
        "def drawFigure():",
        "    df = px.data.iris()",
        "    return html.Div([",
        "        dbc.Card(",
        "            dbc.CardBody([",
        "                dcc.Graph(",
        "                    figure=px.bar(df, x='sepal_width', y='sepal_length', color='species')",
        "                        .update_layout(",
        "                            template='plotly_dark',",
        "                            plot_bgcolor='rgba(0, 0, 0, 0)',",
        "                            paper_bgcolor='rgba(0, 0, 0, 0)',",
        "                        ),",
        "                    config={'displayModeBar': False}",
        "                )",
        "            ])",
        "        ),",
        "    ])",
        "",
        "def drawText(content='Text'):",
        "    return html.Div([",
        "        dbc.Card(",
        "            dbc.CardBody([",
        "                html.Div([",
        "                    html.H2(content),",
        "                ], style={'textAlign': 'center'})",
        "            ])",
        "        ),",
        "    ])",
        "",
        "def drawTable():",
        "    return html.Div([",
        "        dbc.Card(",
        "            dbc.CardBody([",
        "                html.Table([",
        "                    html.Thead([",
        "                        html.Tr([",
        "                            html.Th('Column 1'),",
        "                            html.Th('Column 2'),",
        "                        ])",
        "                    ]),",
        "                    html.Tbody([",
        "                        html.Tr([",
        "                            html.Td('Value 1'),",
        "                            html.Td('Value 2'),",
        "                        ])",
        "                    ])",
        "                ])",
        "            ])",
        "        ),",
        "    ])",
        "",
        "app = Dash(external_stylesheets=[dbc.themes.SLATE])",
        "app.layout = html.Div([",
        "    dbc.Row([",
        "        dbc.Col(drawText('Dashboard Title'), width=12),",
        "    ], align='center'),"
    ]

    components = []
    for widget in widgets:
        if widget['type'] == 'Chart':
            components.append(PlotlyChart(width=widget.get('width', 6)))
        elif widget['type'] == 'Text Block':
            components.append(PlotlyTextBlock(content=widget.get('content', 'Default Text'), width=widget.get('width', 6)))
        elif widget['type'] == 'Table':
            components.append(PlotlyTable(width=widget.get('width', 6)))

    for component in components:
        code_lines += component.generate_code()

    code_lines += [
        "])",
        "",
        "if __name__ == '__main__':",
        "    app.run_server(debug=True)"
    ]
    
    return "\n".join(code_lines)

@app.route('/export', methods=['POST'])
def export_dashboard():
    widgets = request.get_json()
    python_code = generate_plotly_code(widgets)

    response = make_response(python_code)
    response.headers['Content-Disposition'] = 'attachment; filename=dashboard.py'
    response.headers['Content-Type'] = 'text/plain'
    return response

if __name__ == "__main__":
    app.run(debug=True)
