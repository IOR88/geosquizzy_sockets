import unittest
import sys
import time

from gs_socket_tests.utils import TestThread
from gs_socket.base_socket import BaseSocket


class SocketServerInitialization(unittest.TestCase):

    def test_socket_server_init_failure(self):
        """
        Trigger BaseSocket class error during initialization
        """
        self.assertRaises(Exception, BaseSocket, TYPE=None)

    def test_socket_server_init_success(self):
        """
        Checking if socket object has all needed properties
        """
        socket_object_keys = ['accept', 'bind', 'close', 'connect', 'recv', 'send', 'shutdown']
        server_socket = BaseSocket()
        [self.assertTrue(x in server_socket.__dir__()) for x in socket_object_keys]
        server_socket.close_unix_socket()

    def test_socket_server_full_init(self):
        server_socket = BaseSocket()
        server_socket.bind(server_socket.SOCKET_FILE)
        server_socket.listen(server_socket.CONNECTIONS)
        server_socket.close_unix_socket()


class SocketServerClientCommunication(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ADDRESS = '/tmp/baseSocketTest.sock'
        cls.MSG0 = b'Hello, world'
        cls.MSG1 = b'Nice Work!'
        cls.server = BaseSocket(SOCKET_FILE=cls.ADDRESS)
        cls.client = BaseSocket()

    def setUP(self):
        pass

    def test_sockets_connection(self):
        """
        It starts socket server in separate thread, then client socket is connecting to it and
        sending MSG0, assertEqual is made, then server send back MSG1, second assertEqual is made
        """
        def server_run_action(context, msg):
            context.server.bind(context.server.SOCKET_FILE)
            context.server.listen(context.server.CONNECTIONS)
            conn, addr = context.server.accept()
            data = conn.recv(1024)
            context.assertEqual(data, msg)
            conn.sendall(context.MSG1)
            return

        server_thread = TestThread(run=lambda: server_run_action(self, self.MSG0), daemon=True)
        server_thread.start()

        time.sleep(0.1)

        self.client.connect(self.ADDRESS)
        self.client.sendall(self.MSG0)
        data = self.client.recv(1024)
        self.assertEqual(data, self.MSG1)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.client.close()
        cls.server.close_unix_socket()


def test_suite():
    # the warning ignore was added because probably unittest is not aware of socket condition in thread
    unittest.main(warnings='ignore')
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')