import requests

from config import *


# todo move to RedForester UI


def run():
    # make a call to the RedForester to register this extension
    resp = requests.post(f'{EXT_PROXY_BASE_URL}/extensions', json={
        "name": EXT_NAME,
        "description": EXT_DESCRIPTION,
        "baseUrl": f"http://{EXT_BASE_URL}:{EXT_PORT}",
        "email": EXT_EMAIL,
        "commands": [
            {
                "name": "Hello, World!",
                "id": "hello-world",
                "description": "Simple test command description"
            },
            {
                "name": "Failed 'Hello, World!'",
                "id": "failing-hello-world",
                "description": "Always failing command"
            }
        ]
    }, headers={
        'Cookie': USER_COOKIE
    })
    if resp.ok:
        print(f"success, extension data = {resp.json()}")
    else:
        print(f"error, status code = {resp.status_code}, message = {resp.text}")


if __name__ == '__main__':
    run()
