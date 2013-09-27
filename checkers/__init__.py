# -*- coding: utf8
import os

from lightpanel import colors

class BaseChecker(object):
    def __init__(self,
                 success_color=colors.GREEN,
                 failure_color=colors.RED,
                 boot_color=colors.BLUE):

        self._color = boot_color
        self.success_color = success_color
        self.failure_color = failure_color
        self._to_notify = None

    def check(self):
        raise NotImplementedError

    @property
    def status(self):
        return (colors.STATIC, self._color)

    def notify(self):
        pass

    def _speak(sentence, speed = 125, amplitude = 200, voice = 'english-us'):
        os.system("espeak  -s %s -a %s -v %s \"%s\"" % (speed, amplitude, voice, sentence))

    def _play(sound_path):
        os.system("mpg123 %s" % sound_path)

class MultiStatusChecker(BaseChecker):
    status_mapping = {}

    def __init__(*args, **kwargs):
        self.super(*args, **kwargs)
        self._status = None

    @property
    def status(self):
        return self.statuses.get(self._status, (colors.STATIC, self._color))
