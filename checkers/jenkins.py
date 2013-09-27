# -*- coding: utf8
import os
import json
import urllib
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.requester import Requester

from lightpanel import colors
from lightpanel.checkers import MultiStatusChecker

class JeanXV(MultiStatusChecker):
    def __init__(self,
                 jenkins_server,job_name,
                 username=None, password=None,
                 success_color=colors.GREEN,
                 failure_color=colors.RED,
                 stuck_color=colors.GREY):

        self.super(success_color, failure_color)

        self.jenkins_server = jenkins_server
        self.job_name = job_name
        self.username = username
        self.password = password
        self.stuck_color = stuck_color
        self._status = FAILURE

    @property
    def status_mapping(self):
        return {
            'BUILDING':(colors.FADE, self._color),
            'STUCK': (colors.BLINK, self.stuck_color),
            'SUCCESS': (colors.STATIC, self.success_color),
            'ERROR': (colors.STATIC, self.failure_color)
        }


    def check(self):
        if self.username:
            requester = Requester(self.username, self.password, ssl_verify=False)
            jenkins = Jenkins(self.jenkins_server, requester=requester)
        else:
            jenkins = Jenkins(self.jenkins_server)

        job = jenkins[self.job_name]
        if job.is_queued():
            if status['queueItem']['stuck']:
                self._status = 'STUCK'
                return

        build = job.get_last_build()
        if build.is_running():
            self._status = 'BUILDING'
            return

        job_success = build.get_status() == u'SUCCESS'
        status = 'SUCCESS' if job_success else 'FAILURE'

        if status == 'FAILURE' and status != self._status:
            try:
                author_name =  build._data['changeSet']['items'][0]['author']['fullName'].split('.')[0]
                self._to_notify = author_name
            except:
                self._to_notify = ' '
        else:
            self._to_notify = None

        self._status = status
        self._color = self.status_mapping[status][1]

    def notify(self):
        if not self._to_notify:
            return

        self._play("/home/pi/lightpanel/caralarm.mp3")
        self._speak(u"%s t'as tout cassei" % self._to_notify)
        self._to_notify = None
