import requests
import json


with open('message.json', 'r', encoding='utf8') as f:
    data = json.load(f)
    r = requests.post('https://a398-89-175-46-15.eu.ngrok.io/', json=data)