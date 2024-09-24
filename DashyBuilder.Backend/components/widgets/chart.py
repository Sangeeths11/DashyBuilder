from components.widgets.base import Widget
import plotly.express as px
import plotly.graph_objects as go

from components.widgets.chart_types.bar_chart import generate_bar_chart_code
from components.widgets.chart_types.line_chart import generate_line_chart_code
from components.widgets.chart_types.scatter_chart import generate_scatter_chart_code
from components.widgets.chart_types.bubble_chart import generate_bubble_chart_code
from components.widgets.chart_types.pie_chart import generate_pie_chart_code
from components.widgets.chart_types.default_chart import generate_default_chart_code

class ChartWidget(Widget):
    def __init__(self, widget_info, cols, datapath):
        super().__init__(widget_info, cols, datapath)
        self.chart_type = widget_info.get('chartType', 'Pie')
        self.chartconfig = widget_info.get('chartConfig', {})
        
    def generate_code(self):
        self.title = self.name
        self.name = self.name.replace(" ", "")
        self.data = self.df

        chart_type_code = self._generate_chart_code()

        return f"""
def draw{self.chart_type}_{self.name}():
    {chart_type_code}
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    id='{self.name}_{self.chart_type}_graph',
                    figure=fig,
                    config={{'displayModeBar': False}},
                    style={{'height': '100%', 'width': '100%'}},
                    responsive=True
                )
            ]), style={{'height': '100%'}}
        )
    ], style={{'height': '100%', 'padding': '2px'}})
"""

    def _generate_chart_code(self):
        if self.chart_type == 'Bar':
            return generate_bar_chart_code(self.title, self.chartconfig)
        elif self.chart_type == 'Line':
            return generate_line_chart_code(self.title, self.chartconfig)
        elif self.chart_type == 'Scatter':
            return generate_scatter_chart_code(self.title, self.chartconfig)
        elif self.chart_type == 'Bubble':
            return generate_bubble_chart_code(self.title, self.chartconfig)
        elif self.chart_type == 'Pie':
            return generate_pie_chart_code(self.title, self.chartconfig)
        else:
            return generate_default_chart_code(self.title)
