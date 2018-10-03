import logging

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from rf_client import MindMap, set_config
from config import RF_BACKEND_BASE_URL, EXT_PORT


class MapsHandler(RequestHandler):
    def post(self, map_id):
        logging.info(f'Extension assigned to map with id {map_id}')
        self.finish()

    def delete(self, map_id):
        logging.info(f'Extension deleted from map with id {map_id}')
        self.finish()


class IsAliveCommandHandler(RequestHandler):
    def post(self):
        self.finish()


class HelloWorldCommandHandler(RequestHandler):
    async def post(self):
        session = self.request.headers['Session-Id']
        token = self.request.headers['Rf-Extension-Token']
        user_id = self.get_query_argument('userId')
        map_id = self.get_query_argument('mapId')
        node_id = self.get_query_argument('nodeId')

        async with MindMap(map_id, extension_token=token) as mm:
            node = mm.get(node_id)
            node_title = node.body.properties.global_['title']

        self.finish({
            'data': {
                'notify': {
                    'userId': user_id,
                    'session': session,
                    'content': f'Hello, RedForester! user = {user_id}, map = {map_id}, node = {node_id}, node title = {node_title}',
                    'style': 'SUCCESS'
                }
            }
        })


def run():
    logging.basicConfig(
        level=logging.DEBUG
    )

    set_config(RF_BACKEND_BASE_URL)

    app = Application([
        (r'/api/maps/(.+)', MapsHandler),
        (r'/api/commands/is_alive', IsAliveCommandHandler),
        (r'/api/commands/hello-world', HelloWorldCommandHandler),
    ])
    app.listen(EXT_PORT)
    IOLoop.current().start()


if __name__ == '__main__':
    run()