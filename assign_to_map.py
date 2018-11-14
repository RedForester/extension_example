# This is temporary way to assign extension to your map

import logging

import requests
from requests import Response

from config import EXT_PROXY_BASE_URL, USER_COOKIE


def throw_if_error(resp: Response) -> Response:
    if resp.status_code == 200:
        return resp
    raise Exception(f"HTTP error, status = {resp.status_code}, message = {resp.text}")


def run(map_id, node_id_to_test, extension_id):
    try:
        throw_if_error(requests.post(f'{EXT_PROXY_BASE_URL}/extensions/{extension_id}/maps/{map_id}/assign', json={
        }, headers={
            'Cookie': USER_COOKIE
        }, ))
    except Exception as ex:
        logging.warning(str(ex))

    throw_if_error(requests.post(f'{EXT_PROXY_BASE_URL}/extensions/{extension_id}/maps/{map_id}/command', json={
        "commandId": "hello-world",
        "nodeId": node_id_to_test
    }, headers={
        'Cookie': USER_COOKIE
    }))


if __name__ == '__main__':
    run(input("Your map id: "),
        input("Node id to test 'hello-world' command execution: "),
        input("Extension id: "))
