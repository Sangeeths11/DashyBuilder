def generate_numeric_range_filter_code(name):
    return f"""
    html.Div([
        dcc.RangeSlider(
            id='{name}_numeric_slider',
            min=df['sepal_length'].min(),
            max=df['sepal_length'].max(),
            step=0.1,
            marks={{i: str(i) for i in range(int(df['sepal_length'].min()), int(df['sepal_length'].max())+1)}},
            value=[df['sepal_length'].min(), df['sepal_length'].max()],
            tooltip={{'always_visible': True, 'placement': 'bottom'}}
        )
    ], style={{'marginBottom': '20px', 'backgroundColor': '#32383e', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)'}})
    """
