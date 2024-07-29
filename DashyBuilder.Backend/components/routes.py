from flask import jsonify, request, make_response, send_from_directory
import os
import pandas as pd
import subprocess
from ydata_profiling import ProfileReport
from components.dashboard import generate_plotly_code
from components.uploader import FileUploader
import components.hosting as hosting

file_uploader = FileUploader('uploads')

def register_routes(app):
    @app.route('/')
    def hello_geek():
        return '<h1>Hello from Flask & Docker</h1>'

    @app.route('/export', methods=['POST'])
    def export_dashboard():
        data = request.get_json()
        widgets = data.get('widgets', [])
        grid_size = data.get('grid_size', '4x4')
        cloudsave = data.get('save', False)
        python_code = generate_plotly_code(widgets, grid_size)
        response = make_response(python_code)
        response.headers['Content-Disposition'] = 'attachment; filename=dashboard.py'
        response.headers['Content-Type'] = 'text/plain'
        if data.get('save'):
            try:
                with open('dashboards/Dashboard.py', 'w') as f:
                    f.write(python_code)
                return jsonify({'message': 'Dashboard saved successfully'}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        return response

    @app.route('/upload_chunk', methods=['POST'])
    def upload_chunk():
        return file_uploader.upload_chunk()

    @app.route('/finalize_upload', methods=['POST'])
    def finalize_upload():
        return file_uploader.finalize_upload()

    @app.route('/data/<dataset_id>', methods=['GET'])
    def get_dataset(dataset_id):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{dataset_id}.csv")
        if os.path.exists(filepath):
            try:
                chunk_size = 10000
                chunks = pd.read_csv(filepath, chunksize=chunk_size, low_memory=False)

                num_rows = 0
                num_cols = 0
                column_info = None
                missing_values = None
                preview_data = []

                for chunk in chunks:
                    if column_info is None:
                        num_cols = chunk.shape[1]
                        column_info = [{"name": col, "dtype": str(chunk[col].dtype)} for col in chunk.columns]
                        missing_values = chunk.isnull().sum()
                        preview_data = chunk.head(10).fillna('').to_dict(orient='records')
                    else:
                        missing_values += chunk.isnull().sum()
                        if len(preview_data) < 10:
                            preview_data.extend(chunk.head(10 - len(preview_data)).fillna('').to_dict(orient='records'))

                    num_rows += chunk.shape[0]

                data_info = {
                    "num_rows": num_rows,
                    "num_cols": num_cols,
                    "column_info": column_info,
                    "missing_values": missing_values.to_dict(),
                    "preview_data": preview_data,
                }
                return jsonify(data_info)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        return jsonify({'error': 'Dataset not found'}), 404

    @app.route('/profile/<dataset_id>', methods=['GET'])
    def generate_profile(dataset_id):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{dataset_id}.csv")
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath, nrows=5000)
                profile = ProfileReport(
                    df,
                    title=f"Profiling Report for {dataset_id}",
                    minimal=True,
                    explorative=True,
                    pool_size=4
                )
                profile_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{dataset_id}_profile.html")
                profile.to_file(profile_file)
                return send_from_directory(app.config['UPLOAD_FOLDER'], f"{dataset_id}_profile.html")
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        return jsonify({'error': 'Dataset not found'}), 404
    
    @app.route('/upload_to_pythonanywhere', methods=['POST'])
    def upload_to_pythonanywhere():
        data = request.get_json()
        file_path = data.get('file_path')
        if not file_path:
            return jsonify({'error': 'No file_path provided'}), 400
        try:
            return hosting.upload_file_to_pythonanywhere(file_path)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    @app.route('/run-script', methods=['POST'])
    def run_script():
        script_path = 'hostingEndpoint.py'
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
    })
