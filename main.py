import logging
from rf_api_client.rf_api_client import ExtensionAuth

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from rf_api_client import RfApiClient
from rf_client import RfClient
from yarl import URL

from config import RF_BACKEND_BASE_URL, EXT_PORT, EXT_ADDRESS


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

        # This is persistence extension user token. It allow to use RF API from special user (with limitations),
        #  listen event queue.
        # !!! This is single chance to get service token.
        service_token = self.request.headers['Rf-Extension-Token']

        logging.info(f'Extension assigned to map with id {map_id}, service token: {service_token}')

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
        session = self.request.headers.get('Rf-Session-Id')

        # Temporary user token, that allows the extension to access the RedForester API.
        # It will works, while this request is running and will be revoked after request termination.
        user_token = self.request.headers['Rf-Extension-Token']

        # Id of the user, that started this command.
        user_id = self.get_query_argument('userId')

        # Id of the map, that contains the node, on which this command was called.
        map_id = self.get_query_argument('mapId')

        # Id of the node, on which this command was called.
        node_id = self.get_query_argument('nodeId')

        logging.info(f'user_token : {user_token}, user_id: {user_id}, map_id: {map_id}, node_id: {node_id}')

        api = RfApiClient(auth=ExtensionAuth(user_token), session_id=session, base_url=URL(RF_BACKEND_BASE_URL))

        async with RfClient(api) as rf:
            map_ = await rf.maps.load_map(map_id=map_id)
            node = map_.tree.find_by_id(node_id)
            node_title = node.body.properties.global_.title

        # Build response
        self.finish({
            'notify': {
                'userId': user_id,
                'session': session,
                'content': f'Hello, RedForester! user = {user_id}, map = {map_id}, node = {node_title} (id: {node_id})',
                'style': 'SUCCESS'
            }
        })


class FailingHelloWorldCommandHandler(RequestHandler):
    async def post(self):
        """
        This is an another command handler example, that always terminates with error.
        """

        status, code = 400, 100

        self.set_status(status)
        self.finish({
            'code': code,  # TODO error code system support
            'message': f'something failed with code {code}'
        })


def run():
    logging.basicConfig(
        level=logging.DEBUG
    )

    # init tornado handlers
    app = Application([
        (r'/api/maps/(.+)', MapsHandler),
        (r'/api/is-alive', IsAliveCommandHandler),
        (r'/api/commands/hello-world', HelloWorldCommandHandler),
        (r'/api/commands/failing-hello-world', FailingHelloWorldCommandHandler),
    ])
    app.listen(EXT_PORT, EXT_ADDRESS)
    logging.info(f'Run on {EXT_ADDRESS}:{EXT_PORT}')

    IOLoop.current().start()


if __name__ == '__main__':
    run()
