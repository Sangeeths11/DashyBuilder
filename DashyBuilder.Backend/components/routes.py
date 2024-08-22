import io
from flask import jsonify, request, make_response, send_from_directory, send_file
import os
import pandas as pd
import subprocess
from ydata_profiling import ProfileReport
from components.dashboard import generate_plotly_code
from components.uploader import FileUploader
import components.hosting as hosting
from openai import OpenAI
import zipfile
import os

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
        datapath = data.get('file_path')
        
        # Generiere den Python-Code für das Dashboard
        python_code = generate_plotly_code(widgets, grid_size, datapath)
        
        dashboard_content = io.StringIO(python_code)
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            zipf.writestr('Dashboard.py', dashboard_content.getvalue())
            print(f'uploads\\{datapath}.csv')
            if os.path.exists(f'uploads\\{datapath}.csv'):
                zipf.write(f'uploads\\{datapath}.csv', arcname=f'{datapath}.csv')
            else:
                return jsonify({'error': 'CSV file not found'}), 404

        zip_buffer.seek(0)
        response = send_file(zip_buffer, as_attachment=True, download_name='dashboard_export.zip', mimetype='application/zip')
        
        return response
    
    @app.route('/exportCode', methods=['POST'])
    def export_code():
        data = request.get_json()
        widgets = data.get('widgets', [])
        grid_size = data.get('grid_size', '4x4')
        datapath = data.get('file_path')
        python_code = generate_plotly_code(widgets, grid_size, datapath)
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
    
    @app.route('/ai/<dataset_id>', methods=['GET'])
    def get_datasetInfo(dataset_id):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{dataset_id}.csv")
        if os.path.exists(filepath):
            try:
                chunk_size = 10000
                chunks = pd.read_csv(filepath, chunksize=chunk_size, low_memory=False)

                column_info = None
                preview_data = []

                for chunk in chunks:
                    if column_info is None:
                        column_info = [{"name": col, "dtype": str(chunk[col].dtype)} for col in chunk.columns]
                        preview_data = chunk.head(10).fillna('').to_dict(orient='records')
                    else:
                        if len(preview_data) < 10:
                            preview_data.extend(chunk.head(10 - len(preview_data)).fillna('').to_dict(orient='records'))


                data_info = {
                    "column_info": column_info,
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

    @app.route('/ai/openai-process', methods=['POST'])
    def process_openai():
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract necessary information
        column_names = data.get('column_info')
        preview_data = data.get('preview_data')
        research_question = data.get('research_question')
        
        if not column_names or not preview_data or not research_question:
            return jsonify({"error": "Missing required data to process the request"}), 400

        # Load the prompt template
        with open('promptEngineering\\suggestionComponentUser.txt', 'r') as file:
            prompt_template = file.read()

        # Convert column names and preview data into the expected format
        column_names_str = str([col['name'] for col in column_names])
        preview_data_str = str(preview_data)

        # Replace placeholders in the template with actual data
        prompt = prompt_template.replace("[QUESTION]", research_question)
        prompt = prompt.replace("Column Names: []", f"Column Names: {column_names_str}")
        prompt = prompt.replace("Sample Data: []", f"Sample Data: {preview_data_str}")
        
        with open('promptEngineering\\suggestionComponentSystem.txt', 'r') as file:
            prompt_system = file.read()

        #write the new prompt to a file as a backup
        with open('promptEngineering\\suggestionComponentPromptNew.txt', 'w', encoding='utf-8') as file:
            file.write(prompt)

        # OpenAI API call
        try:
            client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
            response  = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.1,
                response_format= {"type": "json_object"},
            )
            result = response.choices[0].message.content
            return jsonify({"result": result})

        except Exception as e:
            return jsonify({"error": str(e)}), 500
