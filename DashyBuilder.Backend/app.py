from flask import Flask, request, make_response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, expose_headers=['Content-Disposition'])

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h1>'

def parse_grid_positions(grid_position_str, cols):
    """Extracts grid positions and calculates the column and row spans."""
    positions = list(map(int, grid_position_str.split(',')))
    rows = [(pos - 1) // cols + 1 for pos in positions]  # Dynamic column grid
    cols = [(pos - 1) % cols + 1 for pos in positions]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    row_span = max_row - min_row + 1
    col_span = max_col - min_col + 1
    return min_row, min_col, row_span, col_span


def generate_plotly_code(widgets, grid_size):
    rows, cols = map(int, grid_size.split('x'))
    code_lines = [
        "from dash import Dash, dcc, html",
        "import dash_bootstrap_components as dbc",
        "import plotly.express as px",
        "import pandas as pd",
        "",
        "# Example table data",
        "table_data = {",
        "    'Spalte 1': [1, 2, 3, 4],",
        "    'Spalte 2': ['A', 'B', 'C', 'D'],",
        "    'Spalte 3': [10.1, 20.2, 30.3, 40.4]",
        "}",
        "table_df = pd.DataFrame(table_data)",
        "",
        "# Load data",
        "df = px.data.iris()",
        "",
        "# Create a graph card",
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
        "                    config={'displayModeBar': False},",
        "                    style={'height': '100%', 'width': '100%'}",
        "                )",
        "            ]),style={'height': '100%'}",
        "        )",
        "    ], style={'height': '100%', 'padding': '2px'})",
        "",
        "# Create a table card",
        "def drawTable():",
        "    return html.Div([",
        "        dbc.Card(",
        "            dbc.CardBody([",
        "                html.Div([",
        "                    dbc.Table.from_dataframe(table_df, striped=True, bordered=True, hover=True, dark=True)",
        "                ])",
        "            ]),style={'height': '100%'}",
        "        )",
        "    ], style={'height': '100%', 'padding': '2px'})",
        "",
        "# Initialize app with external stylesheets",
        "app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])",
        "",
        "# Define layout",
        "app.layout = html.Div([",
        "    dbc.Container([",
        "        html.Div(style={",
        "            'display': 'grid',",
        f"            'grid-template-columns': 'repeat({cols}, 1fr)',",
        f"            'grid-template-rows': 'repeat({rows}, 1fr)',",
        "            'gap': '10px',",
        "            'height': '99vh'",
        "        }, children=["
    ]

    for widget in widgets:
        min_row, min_col, row_span, col_span = parse_grid_positions(widget['gridPosition']['gridPosition'], cols)
        component = 'drawFigure()' if widget['type'] == 'Chart' else 'drawTable()'
        code_lines.append(
            f"            html.Div({component}, style={{'grid-column': '{min_col} / span {col_span}', 'grid-row': '{min_row} / span {row_span}', 'padding': '0px'}}),"
        )
    
    # Close the code
    code_lines.append("        ])")
    code_lines.append("    ], fluid=True, style={'height': '100vh', 'padding': '0', 'margin': '0', 'width': '100vw', 'overflow': 'hidden'})")
    code_lines.append("])")
    code_lines.append("if __name__ == '__main__':")
    code_lines.append("    app.run_server(debug=True)")

    return "\n".join(code_lines)

@app.route('/export', methods=['POST'])
def export_dashboard():
    data = request.get_json()
    widgets = data.get('widgets', [])
    grid_size = data.get('grid_size', '3x3')  # Default to 3x3 if not provided
    python_code = generate_plotly_code(widgets, grid_size)
    response = make_response(python_code)
    response.headers['Content-Disposition'] = 'attachment; filename=dashboard.py'
    response.headers['Content-Type'] = 'text/plain'
    return response

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/export', methods=['POST'])
def export_dashboard():
    data = request.get_json()
    widgets = data.get('widgets', [])
    python_code = generate_plotly_code(widgets)
    response = make_response(python_code)
    response.headers['Content-Disposition'] = 'attachment; filename=dashboard.py'
    response.headers['Content-Type'] = 'text/plain'
    return response

if __name__ == "__main__":
    app.run(debug=True)
