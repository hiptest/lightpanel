import jenkins
import sys

if len(sys.argv) != 2:
    print "Usage: " + sys.argv[0] + " <username>"
    sys.exit(1)

username = sys.argv[1]
jean15 = jenkins.JeanXV(None, None)
jean15._to_notify = username
jean15.notify()

