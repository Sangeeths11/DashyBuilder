import requests
import os
from dotenv import load_dotenv

load_dotenv()

PA_USERNAME = os.getenv('PYTHONANYWHERE_USERNAME')
PA_API_TOKEN = os.getenv('PYTHONANYWHERE_API_KEY')

if not PA_USERNAME or not PA_API_TOKEN:
    raise ValueError("Please set the PYTHONANYWHERE_USERNAME and PYTHONANYWHERE_API_TOKEN environment variables.")

FILE_PATH = os.path.abspath('DashyBuilder.Backend\\dashboards\\Dashboard.py')
FILE_NAME = os.path.basename(FILE_PATH)

if not os.path.exists(FILE_PATH):
    raise FileNotFoundError(f"The file {FILE_PATH} does not exist.")

FILE_UPLOAD_URL = f'https://www.pythonanywhere.com/api/v0/user/{PA_USERNAME}/files/path/home/{PA_USERNAME}/{FILE_NAME}'
WEB_APP_URL = f'https://www.pythonanywhere.com/api/v0/user/{PA_USERNAME}/webapps/'
WSGI_FILE_URL = f'/home/{PA_USERNAME}/{PA_USERNAME}.pythonanywhere.com_wsgi.py'

with open(FILE_PATH, 'rb') as f:
    response = requests.post(
        FILE_UPLOAD_URL,
        files={'content': f},
        headers={'Authorization': f'Token {PA_API_TOKEN}'}
    )
if response.status_code == 200:
    print(f'Uploaded {FILE_NAME} successfully.')
else:
    print(f'Failed to upload {FILE_NAME}: {response.text}')
    exit()

response = requests.post(
    f'{WEB_APP_URL}{PA_USERNAME}.pythonanywhere.com/reload/',
    headers={'Authorization': f'Token {PA_API_TOKEN}'}
)
url = f'https://{PA_USERNAME}.pythonanywhere.com/'
if response.status_code == 200:
    print('Web app reloaded successfully.', url)
else:
    print(f'Failed to reload web app: {response.text}')
