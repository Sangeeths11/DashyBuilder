import requests
import os
from dotenv import load_dotenv
from flask import jsonify

def load_env_variables():
    load_dotenv()

    pa_username = os.getenv('PYTHONANYWHERE_USERNAME')
    pa_api_token = os.getenv('PYTHONANYWHERE_API_KEY')

    if not pa_username or not pa_api_token:
        raise ValueError("Please set the PYTHONANYWHERE_USERNAME and PYTHONANYWHERE_API_TOKEN environment variables.")

    return pa_username, pa_api_token

def upload_file_to_pythonanywhere(file_path):
    pa_username, pa_api_token = load_env_variables()

    file_name = os.path.basename(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    file_upload_url = f'https://www.pythonanywhere.com/api/v0/user/{pa_username}/files/path/home/{pa_username}/{file_name}'
    web_app_url = f'https://www.pythonanywhere.com/api/v0/user/{pa_username}/webapps/'
    wsgi_file_url = f'/home/{pa_username}/{pa_username}.pythonanywhere.com_wsgi.py'

    with open(file_path, 'rb') as f:
        response = requests.post(
            file_upload_url,
            files={'content': f},
            headers={'Authorization': f'Token {pa_api_token}'}
        )
    if response.status_code == 200:
        upload_result = f'Uploaded {file_name} successfully.'
    else:
        return jsonify({'error': f'Failed to upload {file_name}: {response.text}'}), 500

    response = requests.post(
        f'{web_app_url}{pa_username}.pythonanywhere.com/reload/',
        headers={'Authorization': f'Token {pa_api_token}'}
    )
    url = f'https://{pa_username}.pythonanywhere.com/'
    if response.status_code == 200:
        reload_result = 'Web app reloaded successfully.'
        return jsonify({'message': upload_result, 'url': url, 'reload_result': reload_result})
    else:
        return jsonify({'error': f'Failed to reload web app: {response.text}'}), 500
