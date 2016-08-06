class GenericSocketActions:

    def action_close(self):
        self.close_unix_socket()

    def gather_msg(self, chunk, conn, size):
        buffer = chunk
        while True:
            if self.is_msg_completed(buffer):
                break

            buffer += conn(size)

        return buffer


class ServerSocketActions(GenericSocketActions):

    def action_bind(self):
        try:
            self.bind(self.SOCKET_FILE)
        except (Exception, ) as err:
            raise Exception('Exception raised during socket binding')

    def action_listen(self):
        self.listen(self.CONNECTIONS)

    def action_accept(self):
        """
        :return: conn, address
                 :api READ  conn.recv()
                      WRITE conn.send()
        """
        return self.accept()


class ClientSocketActions(GenericSocketActions):

    def action_connect(self):
        try:
            self.connect(self.SOCKET_FILE)
        except (Exception, ) as err:
            raise Exception('Exception raised during socket connection')

    def action_write(self, data):
        self.send(data)

    def action_read(self, size):
        return self.recv(size)

    def action_disconnect(self):
        self.close()