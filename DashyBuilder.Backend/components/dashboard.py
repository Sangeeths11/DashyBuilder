from components.widgets.chart import ChartWidget
from components.widgets.table import TableWidget
from components.widgets.text_block import TextBlockWidget
from components.widgets.filter_box import FilterBoxWidget

def generate_plotly_code(widgets, grid_size):
    rows, cols = map(int, grid_size.split('x'))
    widget_classes = {
        'Chart': ChartWidget,
        'Table': TableWidget,
        'Text Block': TextBlockWidget,
        'Filter Box': FilterBoxWidget
    }
    function_definitions = []
    layout_components = []

    code_header = [
        "from dash import Dash, dcc, html, Input, Output",
        "import dash_bootstrap_components as dbc",
        "import plotly.express as px",
        "import pandas as pd",
        "import warnings",
        "",
        "warnings.filterwarnings('ignore', category=FutureWarning)",
        "table_data = {",
        "    'Spalte 1': [1, 2, 3, 4],",
        "    'Spalte 2': ['A', 'B', 'C', 'D'],",
        "    'Spalte 3': [10.1, 20.2, 30.3, 40.4]",
        "}",
        "table_df = pd.DataFrame(table_data)",
        "df = px.data.iris()",
        "app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])",
        ""
    ]

    for widget in widgets:
        widget_type = widget['type']
        widget_class = widget_classes.get(widget_type)
        if widget_class:
            widget_instance = widget_class(widget, cols)
            function_definitions.append(widget_instance.generate_code())
            widget_name = widget_type.replace(" ", "")
            layout_component = (
                    f"            html.Div(draw{widget_name}_{widget_instance.name}(), "
                    f"style={{'gridColumn': '{widget_instance.min_col} / span {widget_instance.col_span}', "
                    f"'gridRow': '{widget_instance.min_row} / span {widget_instance.row_span}', 'padding': '0px'}}),"
            )
            layout_components.append(layout_component)

    layout_definition = [
        "app.layout = html.Div([",
        "    dbc.Container([",
        "        html.Div(style={",
        "            'display': 'grid',",
        f"           'gridTemplateColumns': 'repeat({cols}, 1fr)',",
        f"           'gridTemplateRows': 'repeat({rows}, 1fr)',",
        "            'gap': '10px',",
        "            'height': '99vh'",
        "        }, children=[",
        "\n".join(layout_components),
        "        ])",
        "    ], fluid=True, style={'height': '100vh', 'padding': '0', 'margin': '0', 'width': '100vw', 'overflow': 'hidden'})",
        "])"
    ]

    server_start = [
        "if __name__ == '__main__':",
        "    app.run_server(debug=True)"
    ]

    full_code = "\n".join(code_header + function_definitions + layout_definition + server_start)
    return full_code
