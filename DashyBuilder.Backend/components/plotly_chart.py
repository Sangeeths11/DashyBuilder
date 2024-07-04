from .plotly_component import PlotlyComponent # type: ignore

class PlotlyChart(PlotlyComponent):
    def __init__(self, width=6):
        self.width = width

    def generate_code(self):
        return [
            "dbc.Col(drawFigure(), width={width}),".format(width=self.width)
        ]
