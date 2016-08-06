import json


class BaseProtocol:
    MSG_TAG_SIZE = 5
    MSG_START_TAG = b"<"*MSG_TAG_SIZE
    MSG_END_TAG = b">"*MSG_TAG_SIZE

    @classmethod
    def is_msg_completed(cls, data):
        return data[data.__len__() - cls.MSG_TAG_SIZE:] == cls.MSG_END_TAG

    @classmethod
    def prepare_msg(cls, msg, decode=None, encode=None):
        """
        :param msg: b""
        :return: decoded or encoded msg
        """
        if decode:
            return msg.decode()
        elif encode:
            return msg.encode()

    @classmethod
    def interpret_msg(cls, msg):
        """
        :msg str()
        :return dict(data: data_length: type:)
        """
        pass

    @classmethod
    def weight_msg(cls, data):
        return data.__sizeof__()

    @classmethod
    def create_msg(cls, data, msg_type=None):
        # http://www.devdungeon.com/content/working-binary-data-python
        # https://pymotw.com/2/struct/
        """
        :arg data dict()
        :keyword msg_type int(0, 1...)
        """
        msg_data = "DATA:{0}".format(json.dumps(data, sort_keys=True))
        msg_data_len = "DATA LENGTH:{0}".format(cls.weight_msg(msg_data))
        msg_type = "TYPE:{0}".format(msg_type)

        return cls.MSG_START_TAG.decode() + ";".join([msg_type, msg_data_len, msg_data]) + cls.MSG_END_TAG.decode()