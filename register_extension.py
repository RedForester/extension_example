import requests

from config import EXT_PROXY_BASE_URL, USER_COOKIE, EXT_BASE_URL, EXT_PORT


# todo move to RedForester UI


def run():
    # make a call to the RedForester to register this extension
    resp = requests.post(f'{EXT_PROXY_BASE_URL}/extensions', json={
        "name": "test-extension",
        "description": "test extension description",
        "baseUrl": f"http://{EXT_BASE_URL}:{EXT_PORT}",
        "email": "test@localhost",
        "commands": [
            {
                "name": "Hello, World!",
                "id": "hello-world",
                "description": "test command description"
            }
        ]
    }, headers={
        'Cookie': USER_COOKIE
    })
    if resp.status_code == 200:
        data = resp.json()
        print(f"success, extension id = {data['data']['id']}")
    else:
        print(f"error, status code = {resp.status_code}, message = {resp.text()}")


if __name__ == '__main__':
    run()