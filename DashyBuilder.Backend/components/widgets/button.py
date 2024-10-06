from components.widgets.base import Widget

class ButtonWidget(Widget):
    def __init__(self, widget_info, cols, datapath):
        super().__init__(widget_info, cols, datapath)
        self.buttonconfig = widget_info.get('buttonConfig', {})
        self.title = self.buttonconfig.get('buttonText', 'Button')
        self.color = self.buttonconfig.get('color', 'primary')
        self.size = self.buttonconfig.get('size', 'md')

    def generate_code(self):
        self.title = self.name
        self.name = self.name.replace(" ", "")
        return f"""
def drawButton_{self.name}(text='{self.title}', color='{self.color}', size='{self.size}', n_clicks=0):
    return html.Div([
        dbc.Button(
            text,
            color=color,
            size=size,
            n_clicks=n_clicks,
            style={{'width': '100%', 'height': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}}
        )
    ], style={{'height': '100%', 'padding': '2px'}})
"""
