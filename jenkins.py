# -*- coding: utf8
import os
import json
import re
import urllib

import colors
from checker import BaseChecker
try:
    from config import SPEAK_SUBSTITUTION
except ImportError:
    SPEAK_SUBSTITUTION = {}
try:
    from config import AUTHOR_NAME_SUBSTITUTION
except ImportError:
    AUTHOR_NAME_SUBSTITUTION = {}

FAILURE = 0
SUCCESS = 1
BUILDING = 2
STUCK = 3

class JeanXV(BaseChecker):
    def __init__(self,
                 jenkins_server,job_name,
                 username=None, password=None,
                 success_color=colors.GREEN,
                 failure_color=colors.RED,
                 stuck_color=colors.GREY):

        self.jenkins_server = jenkins_server
        self.job_name = job_name
        self.username = username
        self.password = password

        self.success_color = success_color
        self.failure_color = failure_color
        self.stuck_color = stuck_color

        self._status = FAILURE
        self._color = colors.BLUE
        self._to_notify = None

    def build_url(self, job_id=None):
        base =  '%s/job/%s%s/api/json' % (
            self.jenkins_server,
            self.job_name,
            '/%s' % job_id if job_id else '')

        if not self.username:
            return base

        return base.replace('://',
                            '://%s:%s@' % (self.username, self.password))

    def json_build(self, url):
        try:
            return json.load(urllib.urlopen(url))
        except Exception as e:
            print '-----------------------'
            print url
            print e

    def check(self):
        status = self.json_build(self.build_url())
        last_build_id = status['lastBuild']['number']

        if status['queueItem'] is not None:
            if status['queueItem']['stuck']:
                self._status = STUCK
                return

        job_status = self.json_build(self.build_url(last_build_id))
        if job_status['building']:
            self._status = BUILDING
            return

        job_success = job_status['result'] == u'SUCCESS'
        status = SUCCESS if job_success else FAILURE

        if status == FAILURE and status != self._status:
            try:
                author_name = job_status['changeSet']['items'][0]['author']['fullName']
                self._to_notify = get_real_name(author_name)
            except:
                print job_status
                self._to_notify = ' '
        else:
            self._to_notify = None

        self._status = status

    def notify(self):
        if not self._to_notify:
            return

        os.system("mpg123 /home/pi/lightpanel/caralarm.mp3")
        text = u"%s t'as tout cassei" % self._to_notify
        text = self.replace_speak_patterns(text)
        os.system("espeak  -s 125 -a 200 -v french \""+text+"\" ")
        self._to_notify = None

    def get_real_name(self, author_name):
        default_name = author_name.split('.')[0]
        return AUTHOR_NAME_SUBSTITUTION.get(author_name, default_name)

    def replace_speak_patterns(self, s):
        keys = [re.escape(key) for key in SPEAK_SUBSTITUTION.keys()]
        if not keys:
            return s
        pattern = re.compile(r'\b(' + '|'.join(keys) + r')\b')
        return pattern.sub(lambda x: SPEAK_SUBSTITUTION[x.group()], s.lower())

    @property
    def status(self):
        if self._status == BUILDING:
            return (colors.FADE, self._color)

        if self._status == STUCK:
            return (colors.BLINK, self.stuck_color)

        if self._status == SUCCESS:
            self._color = self.success_color
        else:
            self._color = self.failure_color

        return (colors.STATIC, self._color)
