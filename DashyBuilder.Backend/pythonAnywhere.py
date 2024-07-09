import requests
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('PYTHONANYWHERE_USERNAME')
token = os.getenv('PYTHONANYWHERE_API_KEY')

if not username or not token:
    raise ValueError("Please set the PYTHONANYWHERE_USERNAME and PYTHONANYWHERE_API_TOKEN environment variables.")

response = requests.get(
    f'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/',
    headers={'Authorization': f'Token {token}'}
)

if response.status_code == 200:
    print('CPU quota info:')
    print(response.content)
else:
    print(f'Got unexpected status code {response.status_code}: {response.content!r}')
