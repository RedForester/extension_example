import logging

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from rf_client import MindMap, set_config
from config import RF_BACKEND_BASE_URL, EXT_PORT


class MapsHandler(RequestHandler):
    def post(self, map_id):
        """
        This method handles assigning the extension to the map.
        Here, the extension can verify, that the map is satisfying some preconditions.
        It can be required types, nodes, etc.
        If everything is OK, the handler must response with the status 200.
        Otherwise, the handler can response with the status 400 and the body, which will describe the problem.
        This handler will be called at the extension registration to verify,
        that the extension is up and works.
        :param map_id: id of the map
        """
        logging.info(f'Extension assigned to map with id {map_id}')
        self.finish()

    def delete(self, map_id):
        """
        This method handles removing the extension from the map.
        If the extension have some data associated to the map, it must be deleted here.
        All subsequent requests to the map will be rejected with 403 status.
        This handler will be called at the extension registration to verify,
        that the extension is up and works.
        :param map_id: id of the map
        """
        logging.info(f'Extension deleted from map with id {map_id}')
        self.finish()


class IsAliveCommandHandler(RequestHandler):
    def post(self):
        """
        This is a command handler. It will be called only at the extension registration to verify,
        that the extension is up and works.
        It must return status 200, if the extension is works.
        """
        self.finish()


class HelloWorldCommandHandler(RequestHandler):
    async def post(self):
        """
        This is an example command handler, that returns request arguments and the title of the node,
        at which it was called.
        """

        # User session, that allows to send notifications back to the user interface in the browser
        session = self.request.headers['Session-Id']

        # Extension token, that allows the extension to access the RedForester API.
        # It will works, while this request is running and for some amount of time after.
        token = self.request.headers['Rf-Extension-Token']

        # Id of the user, that started this command.
        user_id = self.get_query_argument('userId')

        # Id of the map, that contains the node, on which this command was called.
        map_id = self.get_query_argument('mapId')

        # Id of the node, on which this command was called.
        node_id = self.get_query_argument('nodeId')

        # Load whole map by map_id to get node title
        # TODO method for loading single node
        async with MindMap(map_id, extension_token=token) as mm:
            node = mm.get(node_id)
            node_title = node.body.properties.global_['title']

        # Build response
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

    # set base url of the RedForester API
    set_config(RF_BACKEND_BASE_URL)

    # init tornado handlers
    app = Application([
        (r'/api/maps/(.+)', MapsHandler),
        (r'/api/commands/is_alive', IsAliveCommandHandler),
        (r'/api/commands/hello-world', HelloWorldCommandHandler),
    ])
    app.listen(EXT_PORT)
    IOLoop.current().start()


if __name__ == '__main__':
    run()