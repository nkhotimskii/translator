class CountLogger(object):
    def __init__(self):
        self._count = 0

    def log(self):
        self._count += 1