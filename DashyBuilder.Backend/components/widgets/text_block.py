from components.widgets.base import Widget

class TextBlockWidget(Widget):
    def generate_code(self):
        self.name = self.name.replace(" ", "")
        self.text = self.name
        return f"""
def drawTextBlock_{self.name}(text='{self.text}'):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.H4(text, style={{'textAlign': 'center', 'color': 'white', 'height': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}})
            ]), style={{'height': '100%'}}
        )
    ], style={{'height': '100%', 'padding': '2px'}})
"""
