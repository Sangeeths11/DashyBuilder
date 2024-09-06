def generate_pie_chart_code(title):
    return f"""
    fig = px.pie(df, names='species', values='sepal_length').update_layout(
        title={{'text': '{title}', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'}},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    """

# Pie Eingabe Wert:
# names,
# values,