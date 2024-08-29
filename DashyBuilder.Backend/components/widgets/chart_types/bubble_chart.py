def generate_bubble_chart_code(title):
    return f"""
    fig = px.scatter(df, x='sepal_length', y='sepal_width', size='petal_length', color='species').update_layout(
        title={{'text': '{title}', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'}},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    """

# Bubble Eingabe Wert:
# x,
# y,
# size,
# color,