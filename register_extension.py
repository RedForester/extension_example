import hashlib

import requests
from requests.auth import HTTPBasicAuth

from config import *


ext = {
    "name": EXT_NAME,
    "description": EXT_DESCRIPTION,
    "baseUrl": EXT_BASE_URL,
    "email": EXT_EMAIL,
    "commands": [
        {
            "name": "Hello, World!",
            "type": {
                "action": "hello-world",
            },
            "description": "Simple test command description",
            "showRules": [{
                "allNodes": True,
            }],
        },
        {
            "name": "Failed 'Hello, World!'",
            "type": {
                "action": "failing-hello-world",
            },
            "description": "Always failing command",
            "showRules": [{
                "allNodes": True,
            }],
        }
    ]
}


def register_extension():
    username = input("username:")
    password = input("password:")

    auth = HTTPBasicAuth(
        username,
        hashlib.md5(password.encode()).hexdigest()
    )

    # make a call to the RedForester to register this extension
    resp = requests.post(f'{RF_BACKEND_BASE_URL}/api/extensions', json=ext, auth=auth)

    if resp.ok:
        print(f"success, extension data = {resp.json()}")
    else:
        print(f"error, status code = {resp.status_code}, message = {resp.text}")


if __name__ == '__main__':
    register_extension()
