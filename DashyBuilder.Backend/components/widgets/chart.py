from components.widgets.base import Widget
import plotly.express as px
import plotly.graph_objects as go

class ChartWidget(Widget):
    def __init__(self, widget_info, cols, datapath):
        super().__init__(widget_info, cols, datapath)
        self.chart_type = widget_info.get('chartType', 'Pie Chart')
        print(f"ChartWidget: {self.chart_type}")
        
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
                    id='{self.name}_graph',
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
            return """
    fig = px.bar(df, x='species', y='sepal_length').update_layout(
        title={'text': '"""f'{self.title}'"""', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
            """
        elif self.chart_type == 'Line':
            return """
    fig = px.line(df, x='sepal_length', y='sepal_width').update_layout(
        title={'text': '"""f'{self.title}'"""', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
            """
        elif self.chart_type == 'Scatter':
            return """
    fig = px.scatter(df, x='sepal_length', y='sepal_width', color='species').update_layout(
        title={'text': '"""f'{self.title}'"""', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
            """
        elif self.chart_type == 'Bubble':
            return """
    fig = px.scatter(df, x='sepal_length', y='sepal_width', size='petal_length', color='species').update_layout(
        title={'text': '"""f'{self.title}'"""', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
            """
        elif self.chart_type == 'Pie':
            return """
    fig = px.pie(df, names='species', values='sepal_length').update_layout(
        title={'text': '"""f'{self.title}'"""', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
            """
        else:
            return """
    fig = go.Figure().update_layout(
        title={'text': '"""f'{self.title}'"""', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
            """
