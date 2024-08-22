from components.widgets.base import Widget

class ChartWidget(Widget):
    def __init__(self, widget_info, cols, datapath):
        super().__init__(widget_info, cols, datapath)

    def call_openai_api(self):
        # Prepare the prompt
        research_question = f"What is the best way to visualize the data for '{self.name}'?"
        column_info = [{'name': col} for col in self.df.columns]
        preview_data = self.df.head(5).to_dict(orient='records')

        # Convert column names and preview data into the expected format
        column_names_str = str([col['name'] for col in column_info])
        preview_data_str = str(preview_data)

        # User prompt
        prompt_template = (
            f"Given the following columns and sample data:\n"
            f"Column Names: {column_names_str}\n"
            f"Sample Data: {preview_data_str}\n\n"
            f"{research_question}"
        )
        
        # System prompt
        prompt_system = (
            "You are an AI assistant that helps users visualize data. "
            "Based on the input data, suggest the appropriate columns "
            "for a pie chart where one column is used for labels (names) "
            "and another for values."
        )

        # OpenAI API call
        try:
            print("Calling OpenAI API...")

        except Exception as e:
            raise Exception(f"OpenAI API call failed: {str(e)}")    
    def generate_code(self):
        self.title = self.name
        self.name = self.name.replace(" ", "")
        self.data = self.df

        return f"""
def drawChart_{self.name}():
    fig = px.pie(df, names='species', values='sepal_length').update_layout(
        title={{'text': '{self.title}', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'}},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
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
            ]), style={{'height': '100%'}}
        )
    ], style={{'height': '100%', 'padding': '2px'}})
"""