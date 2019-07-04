# encoding = utf-8

import os
import sys
import time
import datetime
import json
import urllib
import urllib2
#from urllib import urlencode
#from urllib2 import urlopen
#from urllib2 import Request
#from urllib2 import urlparse

# Run
#  /opt/splunk/bin/splunk cmd python checkpythonlibs.py
# Expected results:
#  /opt/splunk/lib/python2.7/urllib.pyc
#  /opt/splunk/lib/python2.7/urllib2.pyc

print(urllib.__file__)
print(urllib2.__file__)
