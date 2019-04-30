import requests

from config import USER_COOKIE, RF_BACKEND_BASE_URL


def call_command(map_id, node_id, extension_id, action):
    resp = requests.post(f'{RF_BACKEND_BASE_URL}/extensions/{extension_id}/maps/{map_id}/command', json={
        "action": action,
        "nodeId": node_id
    }, headers={
        'Cookie': USER_COOKIE
    })

    if not resp.ok:
        print(f'Exception(status = {resp.status_code}):')

    print(resp.json())


if __name__ == '__main__':
    map_id = ""
    node_id = ""
    extension_id = ""

    call_command(map_id=map_id,
                 node_id=node_id,
                 extension_id=extension_id,
                 action="hello-world")

    call_command(map_id=map_id,
                 node_id=node_id,
                 extension_id=extension_id,
                 action="failing-hello-world")
