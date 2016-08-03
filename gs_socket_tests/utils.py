from threading import Thread


class TestThread(Thread):
    def __init__(self, *args, **kwargs):
        self.action = kwargs.get('run')
        super(TestThread, self).__init__()

        if kwargs.get('daemon', False):
            self.daemon = True

    def run(self):
        self.action()