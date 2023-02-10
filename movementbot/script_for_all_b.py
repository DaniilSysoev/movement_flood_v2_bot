import requests
import json


def start_script():
    with open('message.json', 'r', encoding='utf8') as f:
        data = json.load(f)
        print(data)
        r = requests.post('https://9e93-83-242-179-137.eu.ngrok.io/', json=data)