# This is temporary way to assign extension to your map

import requests

from config import RF_BACKEND_BASE_URL, USER_COOKIE


def assign_to_map(map_id, extension_id):
    resp = requests.post(
        f'{RF_BACKEND_BASE_URL}/extensions/{extension_id}/maps/{map_id}/assign',
        json={},
        headers={
            'Cookie': USER_COOKIE
        }
    )
    if not resp.ok:
        print('Exception:')

    print(resp.json())

if __name__ == '__main__':
    map_id = ""
    extension_id = ""

    assign_to_map(map_id=map_id,
        extension_id=extension_id)
