import requests

from config import EXT_PROXY_BASE_URL, USER_COOKIE


def exclude_from_map(map_id, extension_id):
    resp = requests.delete(
        f'{EXT_PROXY_BASE_URL}/extensions/{extension_id}/maps/{map_id}/assign',
        headers={
            'Cookie': USER_COOKIE
        }
    )

    if resp.ok:
        print('Extension excluded from map')

    print(resp.json())


if __name__ == '__main__':
    map_id = ""
    extension_id = ""

    exclude_from_map(map_id, extension_id)
