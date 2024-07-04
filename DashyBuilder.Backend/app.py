from flask import Flask, request, make_response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, expose_headers=['Content-Disposition'])

def generate_plotly_code(widgets):
    return 

@app.route('/export', methods=['POST'])
def export_dashboard():
    widgets = request.get_json()
    python_code = generate_plotly_code(widgets)

    response = make_response(python_code)
    response.headers['Content-Disposition'] = 'attachment; filename=dashboard.py'
    response.headers['Content-Type'] = 'text/plain'
    return response

if __name__ == '__main__':
    app.run(debug=True)
