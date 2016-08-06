import unittest
import sys
import time
import queue

from gs_socket_tests.utils import TestThread
from gs_socket.gs_socket import (GsServerSocket, GsClientSocket,)

MSG = [{str(x): z for x, z in [(y, y) for y in range(20000)]} for a in range(10)]


def make_work(works, current):
    if current.empty():
        if not works.empty():
            w = works.get()
            current.put(w)
            return w
        else:
            return None
    else:
        return current.get()


class ServerClientActions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ADDRESS = '/tmp/baseSocketTest.sock'
        cls.server = GsServerSocket(SOCKET_FILE=cls.ADDRESS)
        cls.client = GsClientSocket(SOCKET_FILE=cls.ADDRESS)
        global MSG
        MSG = [cls.server.prepare_msg(cls.server.create_msg(x, msg_type=0), encode=True) for x in MSG]
        cls.works = queue.Queue()
        [cls.works.put(x) for x in MSG]
        cls.current_work = queue.Queue()

    def setUP(self):
        pass

    def test_sockets_actions(self):
        """
        It starts socket server in separate thread, then client socket is connecting to it and
        sending MSG0, assertEqual is made, then server send back MSG1, second assertEqual is made
        """
        def server_run_action(context, works, current_work):
            context.server.action_bind()
            context.server.action_listen()
            clients = []

            def handle_client(conn, works, current_work, context):
                while works.qsize() or current_work.qsize():
                    chunk = conn.recv(1024)
                    data = context.server.gather_msg(chunk, conn.recv, 1024)
                    w = make_work(works, current_work)
                    if w:
                        context.assertEqual(data, w)
                        current_work.task_done()
                        works.task_done()
                        w = make_work(works, current_work)
                        if w:
                            conn.send(w)
                        else:
                            break
                    else:
                        break
                return

            while works.qsize() or current_work.qsize():
                conn, addr = context.server.action_accept()
                new_client = TestThread(run=lambda: handle_client(conn, works, current_work, context), deamon=True)
                clients.append(new_client)
                new_client.start()
                # new_client.join()
            return

        server_thread = TestThread(run=lambda: server_run_action(self, self.works, self.current_work), daemon=True)
        server_thread.start()

        time.sleep(0.1)

        self.client.action_connect()
        while True:
            w = make_work(self.works, self.current_work)
            if w:
                self.client.action_write(w)
                chunk = self.client.action_read(1024)
                data = self.client.gather_msg(chunk, self.client.action_read, 1024)
                w = make_work(self.works, self.current_work)
                if w:
                    self.assertEqual(data, w)
                    self.current_work.task_done()
                    self.works.task_done()
                else:
                    break
            else:
                break

        self.works.join()
        self.current_work.join()
        # server_thread.join()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.client.action_disconnect()
        cls.server.close_unix_socket()


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')