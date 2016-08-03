
import unittest
import sys

from gs_socket.base_socket import BaseSocket


class SocketServerInitialization(unittest.TestCase):
    """ """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_bind_socket(self):
        pass


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')