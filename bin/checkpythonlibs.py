from __future__ import print_function
# encoding = utf-8

from future import standard_library
standard_library.install_aliases()
import os
import sys
import time
import datetime
import json
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
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
