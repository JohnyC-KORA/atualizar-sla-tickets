import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv() 

CHAT=os.getenv('WEBHOOK')

def web_hook(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = CHAT
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    response = requests.post(url, headers=message_headers, data=json.dumps(message))
    print(f"{now} - Status Code: {response.status_code} - Response: {response.text} - Message: {message}")