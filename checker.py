# -*- coding: utf8

class BaseChecker(object):
    def check(self):
        raise NotImplementedError

    def notify(self):
        pass

    @property
    def status(self):
        raise NotImplementedError

