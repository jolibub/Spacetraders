import os
import json

def read_secrets() -> dict:
    filename = os.path.join('users.json')
    try:
        with open(filename, mode='r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}