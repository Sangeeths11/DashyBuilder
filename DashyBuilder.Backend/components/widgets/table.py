from components.widgets.base import Widget

class TableWidget(Widget):
    def generate_code(self):
        self.title = self.name
        self.name = self.name.replace(" ", "")
        return f"""
def drawTable_{self.name}():
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='#2e3338',  # Etwas dunklerer Grauton für den Header, um sich vom CardBody abzuheben
                    font=dict(color='white', size=14, family='Arial'),  # Weißer Text für Kontrast
                    align='center',
                    height=30),
        cells=dict(values=[df[col] for col in df.columns],
                   fill_color=[['#3b4147', '#434a51']*len(df)],  # Abwechselnde, dunkle Grautöne für die Zellen
                   align='center',
                   font=dict(color='white', size=12, family='Arial'),  # Weißer Text in den Zellen
                   height=25)
    )])

    fig.update_layout(
        title={{'text': '{self.title}', 'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'}},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20),
        height=300  # Höhe anpassen je nach Layout-Anforderungen
    )

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
            ]), style={{'height': '100%', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)', 'borderRadius': '10px', 'backgroundColor': '#32383e'}}
        )
    ], style={{'height': '100%', 'padding': '2px'}})
"""
