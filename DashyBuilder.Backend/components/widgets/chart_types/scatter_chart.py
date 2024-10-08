def generate_scatter_chart_code(title, chartconfig):
    return f"""
    fig = px.scatter(df, x='{chartconfig['xAxis']}', y='{chartconfig['yAxis']}', color='{chartconfig['color']}').update_layout(
        title={{'text': '{title}', 'y':0.95, 'x':0.01, 'xanchor': 'left', 'yanchor': 'top'}},
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    """


# Scatter Eingabe Wert:
# x,
# y,
# color,