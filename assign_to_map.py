# This is temporary way to assign extension to your map

import requests

from config import EXT_PROXY_BASE_URL, USER_COOKIE


def run(map_id, extension_id):
    resp = requests.post(f'{EXT_PROXY_BASE_URL}/extensions/{extension_id}/maps/{map_id}/assign', json={
        }, headers={
            'Cookie': USER_COOKIE
        })

    if not resp.ok:
        print('Exception:')

    print(resp.json())

if __name__ == '__main__':
    map_id = ""
    extension_id = ""

    run(map_id=map_id,
        extension_id=extension_id)
