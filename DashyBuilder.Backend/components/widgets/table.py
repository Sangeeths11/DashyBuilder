from components.widgets.base import Widget

class TableWidget(Widget):
    def generate_code(self):
        self.name = self.name.replace(" ", "")
        return f"""
def drawTable_{self.name}():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dbc.Table.from_dataframe(table_df, striped=True, bordered=True, hover=True, dark=True, responsive=True, style={{'width': '100%', 'overflowY': 'auto'}})
            ]), style={{'height': '100%', 'overflow': 'hidden'}}
        )
    ], style={{'height': '100%', 'padding': '2px'}})
"""
