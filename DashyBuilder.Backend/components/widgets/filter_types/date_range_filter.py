from datetime import datetime, timedelta

def generate_date_range_filter_code(name):
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    return f"""
    html.Div([
        dcc.DatePickerRange(
            id='{name}_date_picker',
            start_date='{start_date_str}',
            end_date='{end_date_str}',
            display_format='YYYY-MM-DD',
            style={{
                'backgroundColor': '#32383e',
                'color': '#ffffff',
                'border': '1px solid #4a4a4a',
                'borderRadius': '5px',
                'width': '100%'
            }}
        )
    ], style={{'marginBottom': '20px'}})
    """
