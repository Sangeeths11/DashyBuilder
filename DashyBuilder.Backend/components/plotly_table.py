from .plotly_component import PlotlyComponent

class PlotlyTable(PlotlyComponent):
    def __init__(self, width=6):
        self.width = width

    def generate_code(self):
        return [
            "dbc.Col(drawTable(), width={width}),".format(width=self.width)
        ]
