from gs_socket.base_socket import BaseSocket
from gs_socket.protocol import BaseProtocol
from gs_socket.socket_actions import (ServerSocketActions, ClientSocketActions)


class GsServerSocket(ServerSocketActions, BaseProtocol, BaseSocket):
    def __init__(self, *args, **kwargs):
        super(GsServerSocket, self).__init__(*args, **kwargs)

    def add_client(self):
        pass

    def handle_client_request(self):
        pass


class GsClientSocket(ClientSocketActions, BaseProtocol, BaseSocket):
    def __init__(self, *args, **kwargs):
        super(GsClientSocket, self).__init__(*args, **kwargs)