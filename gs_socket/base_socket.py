from socket import socket, SHUT_WR, AF_UNIX, SOCK_STREAM
import os


class BaseSocket(socket):
    # https://docs.python.org/3/tutorial/classes.html
    # https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/
    # https://docs.python.org/2/howto/sockets.html
    def __init__(self, **kwargs):
        """
        :param kwargs:
        :return:
        :api it exposes all socket module methods
        """
        self.__FAMILY__ = kwargs.get('FAMILY', AF_UNIX)
        self.__TYPE__ = kwargs.get('TYPE', SOCK_STREAM)
        self.CONNECTIONS = kwargs.get('CONNECTIONS', 1)
        self.SOCKET_FILE = kwargs.get('SOCKET_FILE', '/tmp/baseSocket.sock')
        self.remove_unix_socket()
        self.__create_unix_socket__()

    def __create_unix_socket__(self):
        try:
            super(BaseSocket, self).__init__(family=self.__FAMILY__, type=self.__TYPE__)
        except (Exception,) as err:
            raise Exception('Error during socket initialization', err)
        finally:
            pass

    def close_unix_socket(self):
        try:
            self.shutdown(SHUT_WR)
        except (OSError,) as err:
            pass
        finally:
            self.close()
            self.remove_unix_socket()

    def change_unix_socket_permissions(self):
        # OCTAL BASE PERMISSION
        # we have to set permission on socket so ngnix has access to it
        os.chmod(self.SOCKET_FILE, int("777", 8))

    def remove_unix_socket(self):
        try:
            os.remove(self.SOCKET_FILE)
        except (FileNotFoundError, ) as err:
            pass