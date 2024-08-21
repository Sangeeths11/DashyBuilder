from components.widgets.base import Widget

class ButtonWidget(Widget):
    def generate_code(self):
        self.title = self.name
        self.name = self.name.replace(" ", "")
        return f"""
def drawButton_{self.name}(text='{self.title}', color='primary', size='md', n_clicks=0):
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
