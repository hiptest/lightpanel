import os
from time import time
from config import GRAPHITE_SERVER, GRAPHITE_PORT

def send_to_graphite(key, value):
    now = int(time())
    os.system('echo "%s %s %s" | nc %s %s' % (
            key, value, now, GRAPHITE_SERVER, GRAPHITE_PORT))

