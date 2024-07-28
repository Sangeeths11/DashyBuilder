import os
import pandas as pd
from flask import jsonify, request

class FileUploader:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def upload_chunk(self):
        if 'chunk' not in request.files:
            return jsonify({'error': 'No chunk part'}), 400

        chunk = request.files['chunk']
        chunk_number = request.form['chunkNumber']
        total_chunks = request.form['totalChunks']
        filename = request.form['filename']

        dataset_id = filename.replace('.', '_')
        chunk_folder = os.path.join(self.upload_folder, dataset_id)

        if not os.path.exists(chunk_folder):
            os.makedirs(chunk_folder)

        chunk.save(os.path.join(chunk_folder, f"{chunk_number}.part"))

        return jsonify({'message': 'Chunk uploaded successfully'})

    def finalize_upload(self):
        data = request.get_json()
        filename = data['filename']
        dataset_id = filename.replace('.', '_')
        chunk_folder = os.path.join(self.upload_folder, dataset_id)

        assembled_file_path = os.path.join(self.upload_folder, f"{dataset_id}.csv")
        with open(assembled_file_path, 'wb') as assembled_file:
            for chunk_file_name in sorted(os.listdir(chunk_folder), key=lambda x: int(x.split('.')[0])):
                chunk_file_path = os.path.join(chunk_folder, chunk_file_name)
                with open(chunk_file_path, 'rb') as chunk_file:
                    assembled_file.write(chunk_file.read())
        
        for chunk_file_name in os.listdir(chunk_folder):
            os.remove(os.path.join(chunk_folder, chunk_file_name))
        os.rmdir(chunk_folder)

        return jsonify({'filepath': assembled_file_path, 'datasetId': dataset_id})
