from .plotly_component import PlotlyComponent

class PlotlyTextBlock(PlotlyComponent):
    def __init__(self, content='Default Text', width=6):
        self.content = content
        self.width = width

    def generate_code(self):
        return [
            "dbc.Col(drawText('{content}'), width={width}),".format(content=self.content, width=self.width)
        ]
