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

def parse_grid_position(grid_position):
    return list(map(int, grid_position.split(',')))

def generate_plotly_code(widgets, grid_size):
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
        grid_positions = parse_grid_position(widget['gridPosition']['gridPosition'])
        rows = sorted(set((pos - 1) // int(grid_size[0]) for pos in grid_positions))
        cols = sorted(set((pos - 1) % int(grid_size[0]) for pos in grid_positions))
        
        component_code = ""
        if widget['type'] == 'Chart':
            component_code = "drawFigure()"
        elif widget['type'] == 'Text Block':
            component_code = f"drawText('{widget.get('content', 'Default Text')}')"
        elif widget['type'] == 'Table':
            component_code = "drawTable()"
        
        for row in rows:
            components.append((row, cols, f"dbc.Col({component_code}, width={12 // int(grid_size[0])})"))

    components.sort()  # Sort by row
    current_row = -1
    for row, cols, component_code in components:
        if row != current_row:
            if current_row != -1:
                code_lines.append("    ], align='center'),")
            code_lines.append("    dbc.Row([")
            current_row = row
        code_lines.append(f"        {component_code},")
    code_lines.append("    ], align='center'),")

    code_lines += [
        "])",
        "",
        "if __name__ == '__main__':",
        "    app.run_server(debug=True)"
    ]
    
    return "\n".join(code_lines)

@app.route('/export', methods=['POST'])
def export_dashboard():
    data = request.get_json()
    widgets = data['widgets']
    grid_size = data['grid_size']
    python_code = generate_plotly_code(widgets, grid_size)

    response = make_response(python_code)
    response.headers['Content-Disposition'] = 'attachment; filename=dashboard.py'
    response.headers['Content-Type'] = 'text/plain'
    return response

if __name__ == "__main__":
    app.run(debug=True)
