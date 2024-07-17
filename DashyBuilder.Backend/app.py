from flask import Flask, request, make_response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, expose_headers=['Content-Disposition'])

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h1>'

def parse_grid_positions(grid_positions):
    return [int(pos) - 1 for pos in grid_positions.split(',')]

def generate_plotly_code(widgets, grid_size):
    rows, cols = map(int, grid_size.split('x'))
    code_lines = [
        "from dash import Dash, dcc, html",
        "import dash_bootstrap_components as dbc",
        "import plotly.express as px",
        "import pandas as pd",
        "",
        "# Beispiel-Tabellendaten",
        "table_data = {",
        "    'Spalte 1': [1, 2, 3, 4],",
        "    'Spalte 2': ['A', 'B', 'C', 'D'],",
        "    'Spalte 3': [10.1, 20.2, 30.3, 40.4]",
        "}",
        "table_df = pd.DataFrame(table_data)",
        "",
        "# Daten laden",
        "df = px.data.iris()",
        "",
        "# Erstellt eine Graph-Card",
        "def drawFigure():",
        "    return html.Div([",
        "        dbc.Card(",
        "            dbc.CardBody([",
        "                dcc.Graph(",
        "                    figure=px.bar(",
        "                        df, x='sepal_width', y='sepal_length', color='species'",
        "                    ).update_layout(",
        "                        template='plotly_dark',",
        "                        plot_bgcolor='rgba(0, 0, 0, 0)',",
        "                        paper_bgcolor='rgba(0, 0, 0, 0)',",
        "                        height=250,",
        "                        margin=dict(l=20, r=20, t=20, b=20)",
        "                    ),",
        "                    config={",
        "                        'displayModeBar': False",
        "                    },",
        "                    style={'height': '100%', 'width': '100%'}",
        "                )",
        "            ]),",
        "            style={'height': '100%'}",
        "        ),",
        "    ], style={'height': '100%', 'padding': '2px'})",
        "",
        "# Erstellt eine Text-Card",
        "def drawText(text='Text'):",
        "    return html.Div([",
        "        dbc.Card(",
        "            dbc.CardBody([",
        "                html.Div([",
        "                    html.H4(text),",
        "                ], style={'textAlign': 'center', 'color': 'white', 'height': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})",
        "            ]),",
        "            style={'height': '100%'}",
        "        ),",
        "    ], style={'height': '100%', 'padding': '2px'})",
        "",
        "# Erstellt eine Table-Card",
        "def drawTable():",
        "    return html.Div([",
        "        dbc.Card(",
        "            dbc.CardBody([",
        "                html.Div([",
        "                    dbc.Table.from_dataframe(table_df, striped=True, bordered=True, hover=True, dark=True)",
        "                ])",
        "            ]),",
        "            style={'height': '100%'}",
        "        ),",
        "    ], style={'height': '100%', 'padding': '2px'})",
        "",
        "# App initialisieren mit externen Stylesheets",
        "app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])",
        "",
        "# Layout definieren",
        "app.layout = html.Div([",
        "    dbc.Container(["
    ]

    
    filled_positions = set()

    widgets = sorted(widgets, key=lambda w: parse_grid_positions(w['gridPosition']['gridPosition'])[0])

    for widget in widgets:
        grid_positions = parse_grid_positions(widget['gridPosition']['gridPosition'])
        component_code = ""
        if widget['type'] == 'Chart':
            component_code = "drawFigure()"
        elif widget['type'] == 'Text Block':
            component_code = f"drawText('{widget.get('content', 'Default Text')}')"
        elif widget['type'] == 'Table':
            component_code = "drawTable()"
        
        min_pos = min(grid_positions)
        max_pos = max(grid_positions)
        row_start = min_pos // cols
        row_end = max_pos // cols
        col_start = min_pos % cols
        col_end = max_pos % cols
        row_span = row_end - row_start + 1
        col_span = col_end - col_start + 1
        
        for pos in grid_positions:
            filled_positions.add(pos)

        for row in range(row_start):
            code_lines.append("        dbc.Row([")
            for col in range(cols):
                code_lines.append(f"            dbc.Col(width={12 // cols}, style={{'padding': '0px'}}),")
            code_lines.append("        ], style={'height': '33vh', 'margin': '0px'}),")

        code_lines.append("        dbc.Row([")
        for col in range(cols):
            position = row_start * cols + col
            if col_start <= col <= col_end:
                if col == col_start:
                    width = col_span * (12 // cols)
                    code_lines.append(f"            dbc.Col({component_code}, width={width}, style={{'padding': '0px'}}),")
            else:
                code_lines.append(f"            dbc.Col(width={12 // cols}, style={{'padding': '0px'}}),")
        code_lines.append(f"        ], style={{'height': '{100 // rows * row_span}vh', 'margin': '0px'}}),")

    for row in range(row_end + 1, rows):
        code_lines.append("        dbc.Row([")
        for col in range(cols):
            code_lines.append(f"            dbc.Col(width={12 // cols}, style={{'padding': '0px'}}),")
        code_lines.append("        ], style={'height': '33vh', 'margin': '0px'}),")

    code_lines += [
        "    ], fluid=True, style={'height': '100vh', 'padding': '0', 'margin': '0', 'width': '100vw', 'overflow': 'hidden'})",
        "])",
        "",
        "if __name__ == '__main__':",
        "    app.run_server(debug=True)"
    ]
    
    return '\n'.join(code_lines)

@app.route('/export', methods=['POST'])
def export_dashboard():
    data = request.get_json()
    try:
        widgets = data['widgets']
        grid_size = data['grid_size']
    except KeyError as e:
        return f"Missing key in JSON data: {e}", 400
    
    python_code = generate_plotly_code(widgets, grid_size)

    response = make_response(python_code)
    response.headers['Content-Disposition'] = 'attachment; filename=dashboard.py'
    response.headers['Content-Type'] = 'text/plain'
    return response

if __name__ == "__main__":
    app.run(debug=True)
