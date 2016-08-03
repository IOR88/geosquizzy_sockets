from gs_socket.base_socket import BaseSocket
from gs_socket.protocol import BaseProtocol
from gs_socket.socket_actions import (ServerSocketActions, ClientSocketActions)


class GsServerSocket(ServerSocketActions, BaseProtocol, BaseSocket):
    pass


class GsClientSocket(ClientSocketActions, BaseProtocol, BaseSocket):
    pass




server = GsServerSocket()


server.action_bind()
server.change_unix_socket_permissions()
# chmod 777 baseSocket.sock

server.action_listen()

while True:

    conn, addr = server.action_accept()

    data = conn.recv(1024)

    print('FIRST CLIENT :)', addr)
    print('DATA IS', data)

    # conn.send(b'HTTP/1.0 200 OK\r\n')
    # conn.send(b'Content-Type: text/html\r\n\r\n')
    # conn.send(b'<html><body><h1>Hello World</body></html>')
    conn.sendall(b'HELLO WORLD')


client = GsClientSocket()

# print(server.__dir__())