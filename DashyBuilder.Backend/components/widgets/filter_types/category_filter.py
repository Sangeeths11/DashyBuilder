def generate_category_filter_code(name):
    return f"""
    html.Div([
        dcc.Dropdown(
            id='{name}_category_dropdown',
            options=[
                {{'label': 'Setosa', 'value': 'setosa'}},
                {{'label': 'Versicolor', 'value': 'versicolor'}},
                {{'label': 'Virginica', 'value': 'virginica'}}
            ],
            multi=True,
            style={{
                'backgroundColor': '#32383e',
                'color': '#000000',
                'border': '1px solid #4a4a4a',
                'borderRadius': '5px',
                'width': '100%'
            }}
        )
    ], style={{'marginBottom': '20px', 'backgroundColor': '#32383e', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)'}})
    """
