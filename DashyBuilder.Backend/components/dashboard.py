from components.widgets.chart import ChartWidget
from components.widgets.table import TableWidget
from components.widgets.text_block import TextBlockWidget
from components.widgets.filter_box import FilterBoxWidget
from components.widgets.button import ButtonWidget

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

    code_header = [
        "from dash import Dash, dcc, html, Input, Output",
        "import dash_bootstrap_components as dbc",
        "import plotly.express as px",
        "import plotly.graph_objects as go",
        "import pandas as pd",
        "import warnings",
        "",
        "warnings.filterwarnings('ignore', category=FutureWarning)",
        # ToDO: For Bachelor's Thesis
        # f"df = pd.read_csv('{datapath}.csv')",
        "df = px.data.iris()",
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
    ]

    callbackComponents = []
    callbackComponents.append(
        "@app.callback("
        "\n    Output('asd_graph', 'figure'),"
        "\n    Input('asd_numeric_slider', 'value')"
        "\n)"
        "\ndef update_bar_chart(sepal_length_range):"
        "\n    filtered_df = df[(df['sepal_length'] >= sepal_length_range[0]) & (df['sepal_length'] <= sepal_length_range[1])]"
        "\n    fig = px.bar(filtered_df, x='species', y='sepal_length').update_layout("
        "\n        title={'text': 'Sepal Length per Species', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'},"
        "\n        template='plotly_dark',"
        "\n        plot_bgcolor='rgba(0, 0, 0, 0)',"
        "\n        paper_bgcolor='rgba(0, 0, 0, 0)',"
        "\n        margin=dict(l=20, r=20, t=40, b=20)"
        "\n    )"
        "\n    return fig"
    )

    callback_definitions = [
        "\n".join(callbackComponents)
    ]

    server_start = [
        "if __name__ == '__main__':",
        "    app.run_server(debug=True)"
    ]

    full_code = "\n".join(code_header + function_definitions + layout_definition + callback_definitions + server_start)
    return full_code
