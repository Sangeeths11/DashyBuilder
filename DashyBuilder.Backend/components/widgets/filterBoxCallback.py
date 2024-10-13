class FilterBoxCallback:
    def __init__(self, widget, df_name='df'):
        self.widget = widget
        self.df_name = df_name
        self.name = self.widget.get('name', f'Widget{self.widget.get("id", "")}').replace(" ", "")
        self.name = self.name.replace(" ", "")
        self.filter_types = self.widget.get('filterTypes', [])

    def generate_numeric_range_callback(self):
        return (
            f"@app.callback("
            f"\n    Output('asd_graph', 'figure'),"
            f"\n    Input('{self.name}_numeric_slider', 'value')"
            f"\n)"
            f"\ndef update_numeric_range_chart({self.name}_numeric_slider):"
            f"\n    filtered_df = {self.df_name}[(df['sepal_length'] >= {self.name}_numeric_slider[0]) & (df['sepal_length'] <= {self.name}_numeric_slider[1])]"
            f"\n    fig = px.bar(filtered_df, x='species', y='sepal_length').update_layout("
            f"\n        title={{'text': 'Sepal Length per Species', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'}},"
            f"\n        template='plotly_dark',"
            f"\n        plot_bgcolor='rgba(0, 0, 0, 0)',"
            f"\n        paper_bgcolor='rgba(0, 0, 0, 0)',"
            f"\n        margin=dict(l=20, r=20, t=40, b=20)"
            f"\n    )"
            f"\n    return fig\n"
        )

    def generate_date_range_callback(self):
        return (
            f"@app.callback("
            f"\n    Output('asd_graph', 'figure'),"
            f"\n    Input('{self.name}_date_picker', 'start_date'),"
            f"\n    Input('{self.name}_date_picker', 'end_date')"
            f"\n)"
            f"\ndef update_date_range_chart(start_date, end_date):"
            f"\n    filtered_df = {self.df_name}[(df['date'] >= start_date) & ({self.df_name}['date'] <= end_date)]"
            f"\n    fig = px.bar(filtered_df, x='species', y='sepal_length').update_layout("
            f"\n        title={{'text': 'Sepal Length per Species', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'}},"
            f"\n        template='plotly_dark',"
            f"\n        plot_bgcolor='rgba(0, 0, 0, 0)',"
            f"\n        paper_bgcolor='rgba(0, 0, 0, 0)',"
            f"\n        margin=dict(l=20, r=20, t=40, b=20)"
            f"\n    )"
            f"\n    return fig\n"
        )

    def generate_callbacks(self):
        callbacks = []
        if "Numeric Range" in self.filter_types:
            callbacks.append(self.generate_numeric_range_callback())
        if "Date Range" in self.filter_types:
            callbacks.append(self.generate_date_range_callback())
        return "\n".join(callbacks)
