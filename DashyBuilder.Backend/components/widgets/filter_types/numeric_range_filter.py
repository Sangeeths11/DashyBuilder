def generate_numeric_range_filter_code(name, filterconfig):
    if not filterconfig:
        return f"""
        html.Div([
            dcc.RangeSlider(
                id='{name}_numeric_slider',
                min=0,
                max=100,
                step=0.1,
                marks={{i: str(i) for i in range(0, 101)}},
                value=[0, 100],
                tooltip={{'always_visible': True, 'placement': 'bottom'}}
            )
        ], style={{'marginBottom': '20px', 'backgroundColor': '#32383e', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)'}})
        """
    else:
        coloumn = filterconfig.get('column', '')
        step = filterconfig.get('step', 0.1)
        return f"""
        html.Div([
            dcc.RangeSlider(
                id='{name}_numeric_slider',
                min=df['{coloumn}'].min(),
                max=df['{coloumn}'].max(),
                step={step},
                marks={{i: str(i) for i in range(int(df['{coloumn}'].min()), int(df['{coloumn}'].max())+1)}},
                value=[df['{coloumn}'].min(), df['{coloumn}'].max()],
                tooltip={{'always_visible': True, 'placement': 'bottom'}}
            )
        ], style={{'marginBottom': '20px', 'backgroundColor': '#32383e', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)'}})
        """
