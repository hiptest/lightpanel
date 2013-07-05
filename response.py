# -*- coding: utf8
from time import time
from urllib2 import urlopen

import colors
from utils import bound, byte_bound
from checker import BaseChecker

class Response(BaseChecker):
    def __init__(self, check_url, min_time = 0, max_time = 1, check_number = 10):
        self.check_url = check_url

        self.min_time = float(min_time)
        self.max_time = float(max_time)
        self.check_number = float(check_number)

        self._step = (max_time - min_time) / 255.0
        self._response = max_time

    def check(self):
        responses = []
        for i in range(0, int(self.check_number + 1)):
            now = time()
            index = urlopen(self.check_url)
            if index.getcode() != 200:
                raise ValueError('Incorrect response status')
            responses.append(time() - now)

        self._response = sum(responses) / self.check_number

    @property
    def status(self):
        response = bound(
            self._response,
            self.min_time,
            self.max_time)

        diff = (response - self.min_time) / self._step
        pixel = bytearray(3)
        pixel[0] = byte_bound(diff)
        pixel[1] = byte_bound(254 - diff)
        pixel[2] = 0

        return (colors.STATIC, pixel)
