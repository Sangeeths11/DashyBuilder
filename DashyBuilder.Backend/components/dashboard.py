from components.widgets.chart import ChartWidget
from components.widgets.table import TableWidget
from components.widgets.text_block import TextBlockWidget
from components.widgets.filter_box import FilterBoxWidget
from components.widgets.button import ButtonWidget
from components.widgets.filterBoxCallback import FilterBoxCallback

def generate_plotly_code(widgets, grid_size, datapath):
    cols, rows = map(int, grid_size.split('x'))
    widget_classes = {
        'Chart': ChartWidget,
        'Bar': ChartWidget,
        'Line': ChartWidget,
        'Pie': ChartWidget,
        'Scatter': ChartWidget,
        'Bubble': ChartWidget,
        'Table': TableWidget,
        'Text Block': TextBlockWidget,
        'Filter Box': FilterBoxWidget,
        'Button': ButtonWidget
    }
    function_definitions = []
    layout_components = []
    callback_components = []

    code_header = [
        "from dash import Dash, dcc, html, Input, Output",
        "import dash_bootstrap_components as dbc",
        "import plotly.express as px",
        "import plotly.graph_objects as go",
        "import pandas as pd",
        "import warnings",
        "",
        "warnings.filterwarnings('ignore', category=FutureWarning)",
        
        f"df = pd.read_csv('{datapath}.csv')",
        # "df = px.data.iris()",
        "app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])",
        ""
    ]

    for widget in widgets:
        widget_type = widget['type']
        if widget_type == 'Chart':
           print(f"ChartWidget: {widget['chartType']}")
           widget_type = widget['chartType']
        widget_class = widget_classes.get(widget_type)
        
        if widget_type == 'Filter Box':
            widget_class = widget_classes.get('Filter Box')
            if widget_class:
                widget_instance = widget_class(widget, cols, datapath)
                function_definitions.append(widget_instance.generate_code())
                widget_name = 'FilterBox'
                widget_instance.name = widget_instance.name.replace(" ", "")
                layout_component = (
                    f"            html.Div(draw{widget_name}_{widget_instance.name}(), "
                    f"style={{'gridColumn': '{widget_instance.min_col} / span {widget_instance.col_span}', "
                    f"'gridRow': '{widget_instance.min_row} / span {widget_instance.row_span}', 'padding': '0px'}}),"
                )
                layout_components.append(layout_component)

                callback_generator = FilterBoxCallback(widget)
                callback_components.append(callback_generator.generate_callbacks())

        elif widget_class:
            widget_instance = widget_class(widget, cols, datapath)
            function_definitions.append(widget_instance.generate_code())
            widget_name = widget_type.replace(" ", "")
            widget_instance.name = widget_instance.name.replace(" ", "")
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
        "\n"
    ]

    callback_definitions = [
        "\n".join(callback_components)
    ]

    server_start = [
        "if __name__ == '__main__':",
        "    app.run_server(debug=True)"
    ]

    full_code = "\n".join(code_header + function_definitions + layout_definition + callback_definitions + server_start)
    return full_code
