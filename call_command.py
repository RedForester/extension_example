import requests

from config import USER_COOKIE, EXT_PROXY_BASE_URL


def call_command(map_id, node_id, extension_id, command_id):
    resp = requests.post(f'{EXT_PROXY_BASE_URL}/extensions/{extension_id}/maps/{map_id}/command', json={
        "commandId": command_id,
        "nodeId": node_id
    }, headers={
        'Cookie': USER_COOKIE
    })

    if not resp.ok:
        print('Exception:')

    print(resp.json())


if __name__ == '__main__':
    map_id = ""
    node_id = ""
    extension_id = ""

    call_command(map_id=map_id,
                 node_id=node_id,
                 extension_id=extension_id,
                 command_id="hello-world")

    call_command(map_id=map_id,
                 node_id=node_id,
                 extension_id=extension_id,
                 command_id="failing-hello-world")
