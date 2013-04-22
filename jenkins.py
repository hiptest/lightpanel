import json
import urllib

import colors
import writer
from checker import BaseChecker

class JeanXV(BaseChecker):
    def __init__(self,
                 jenkins_server,job_name,
                 username=None, password=None,
                 success_color=colors.GREEN,
                 failure_color=colors.RED):

        self.jenkins_server = jenkins_server
        self.job_name = job_name
        self.username = username
        self.password = password

        self.success_color = success_color
        self.failure_color = failure_color

    def build_url(self):
        base =  '%s/job/%s/api/json' % (self.jenkins_server,
                                        self.job_name)
        if not self.username:
            return base

        return base.replace('://',
                            '://%s:%s@' % (self.username, self.password))

    def check(self):
        status = json.load(urllib.urlopen(self.build_url()))
        last_build = status['lastCompletedBuild']['number']
        return last_build == status['lastSuccessfulBuild']['number']
        
