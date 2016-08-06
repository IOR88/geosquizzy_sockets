import unittest
import sys

from gs_socket.protocol import BaseProtocol


class ProtocolMethods(unittest.TestCase):

    example_msg_str = "<<<<<TYPE:0;DATA LENGTH:99;DATA:{\"secret_data\": 1, \"secret_momentum\": \"now!\"}>>>>>"
    example_msg_byte = b"<<<<<TYPE:0;DATA LENGTH:99;DATA:{\"secret_data\": 1, \"secret_momentum\": \"now!\"}>>>>>"

    @classmethod
    def setUpClass(cls):
        cls.protocol_instance = BaseProtocol()

    def setUP(self):
        pass

    def test_is_msg_completed(self):
        self.assertTrue(self.protocol_instance.is_msg_completed(b"some data.>>>>>"))

    def test_prepare_msg(self):
        bytes_encoded = self.protocol_instance.prepare_msg(self.example_msg_str, encode=True)
        string_decoded = self.protocol_instance.prepare_msg(self.example_msg_byte, decode=True)
        self.assertEqual(bytes_encoded, self.example_msg_byte)
        self.assertEqual(string_decoded, self.example_msg_str)

    def test_interpret_msg(self):
        pass

    def test_weight_msg(self):
        msg_string = "DATA:{\"secret_data\": 1, \"secret_momentum\": \"now!\"}"
        self.assertEqual(msg_string.__sizeof__(), 99)

    def test_create_msg(self):
        msg = self.protocol_instance.create_msg({'secret_data': 1, 'secret_momentum': 'now!'},
                                                msg_type=0)
        self.assertEqual(msg, self.example_msg_str)
        pass

    @classmethod
    def tearDownClass(cls):
        pass


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')