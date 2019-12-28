
# encoding = utf-8

from future import standard_library
standard_library.install_aliases()
from builtins import str
import os
import sys
import time
import datetime
import json
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.request import Request
from urllib2 import urlparse
from urllib.request import build_opener
from urllib.request import ProxyHandler
from urllib.request import install_opener

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''

# Copyright 2019 Jorrit Folmer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

def is_proxy(helper):
    """ Determine whether or not a proxy is configured """
    try:
        proxy = helper.get_proxy()
        proxies = {}
        if proxy.get('proxy_url', False):
            return True
        else:
            return False
    except Exception as e:
        return False

def get_proxies(helper):
    """ Return a proxy dict from proxy settings in addon """
    proxy = helper.get_proxy()
    proxies = {}
    if proxy.get('proxy_url', False):
        if(proxy["proxy_username"] and proxy["proxy_password"]):
            proxy_url = "%s://%s:%s@%s:%s" % (proxy["proxy_type"], proxy["proxy_username"], proxy["proxy_password"], proxy["proxy_url"], proxy["proxy_port"])
            proxies = {
                "http" : proxy_url,
                "https" : proxy_url
            }
        else:
            proxy_url = "%s://%s:%s" % (proxy["proxy_type"], proxy["proxy_url"], proxy["proxy_port"])
            proxies = {
                "http" : proxy_url,
                "https" : proxy_url
            }
    helper.log_debug("proxies dict is : {}".format(proxies))
    return proxies

def get_defender_connectivity(helper, api_endpoint):
    """ Check basic connectivity after saving new inputs in the addon """
    if is_proxy(helper):
        install_opener(build_opener(ProxyHandler(get_proxies(helper))))
    # Do request
    try:
        url = "https://login.windows.net/" 
        req = Request(url)
        response = urlopen(req)
    except Exception as e:
        raise Exception("Error connecting to %s: %s" % (url, str(e)))
        exit(1)
    else:
        helper.log_info("Succesfully connected to %s" % url)

def get_defender_access_token(helper, client_id, secret, tenant_id):
    """ Returns an oauth2 access token string from login.windows.net 
        given a client_id, secret and tenant_id """

    body = {
        'resource' : 'https://api.securitycenter.windows.com',
        'client_id' : client_id,
        'client_secret' : secret,
        'grant_type' : 'client_credentials'
    }

    # Prepare request
    try:
        url = "https://login.windows.net/%s/oauth2/token" % (tenant_id)
        data = urlencode(body).encode("utf-8")
    except Exception as e:
        raise Exception("Error encoding token request body for client_id %s: %s" % (client_id, str(e)))
        exit(1)
    else:
        helper.log_debug("Succesfully parsed token request prep for %s" % url)

    # Do request
    if is_proxy(helper):
        try:
            proxies = get_proxies(helper)
            install_opener(build_opener(ProxyHandler(proxies)))
        except Exception as e:
            raise Exception("Error setting proxy %s: %s" % (get_proxies(helper), str(e)))
            exit(1)
        else:
            helper.log_debug("Succesfully installed proxies %s" % proxies)
    try:
        helper.log_debug("Sending token request to %s" % url)
        req = Request(url, data)
        response = urlopen(req)
    except Exception as e:
        raise Exception("Error getting token for client_id %s from %s: %s" % (client_id, url, str(e)))
        exit(1)
    else:
        helper.log_info("Succesfully sent token request to %s" % url)
        # Parse request
        try:
            jsonResponse = json.loads(response.read())
            access_token = jsonResponse["access_token"]
        except Exception as e:
            raise Exception("Error parsing token response for client_id %s from %s: %s" % (client_id, url, str(e)))
            exit(1)
        else:
            helper.log_info("Succesfully parsed access_token for client_id %s from o %s" % (client_id, url))
            return access_token

def get_defender_query_results(helper, client_id, access_token, api_endpoint, query):
    headers = { 
	'Content-Type' : 'application/json',
	'Accept' : 'application/json',
	'Authorization' : "Bearer " + access_token
    }

    # Prepare request
    try:
        url = "https://%s/api/advancedqueries/run" % api_endpoint
        data = json.dumps({ 'Query' : query }).encode("utf-8")
    except Exception as e:
        raise Exception("Error encoding query request body for client_id %s: %s" % (client_id, str(e)))
        exit(1)
    else:
        helper.log_debug("Succesfully parsed query request prep for %s" % url)

    # Do request
    if is_proxy(helper):
        try:
            proxies = get_proxies(helper)
            install_opener(build_opener(ProxyHandler(proxies)))
        except Exception as e:
            raise Exception("Error setting proxy %s: %s" % (get_proxies(helper), str(e)))
            exit(1)
        else:
            helper.log_debug("Succesfully installed proxies %s" % proxies)
    try:
        helper.log_debug("Sending query request to %s: %s \n %s\n" % (url, headers, data))
        req = Request(url, data, headers)
        response = urlopen(req)
    except Exception as e:
        # 1) Permission for AdvancedQuery.Read.All under WindowsDefenderATP should be granted
        #    under AAD -> App registrations -> WindowsDefenderATPThreatIntelAPI 
        # 2) Grant permissions by admin should also be run because we can't ok this question panel through the API
        raise Exception("Error getting query results for client_id %s from %s: %s" % (client_id, url, str(e)))
        exit(1)
    else:
        helper.log_info("Succesfully sent query request to %s" % url)
        try:
            jsonResponse = json.loads(response.read())
            #schema = jsonResponse["Schema"]
            results = jsonResponse["Results"]
        except Exception as e:
            raise Exception("Error parsing query response for client_id %s from %s: %s" % (client_id, url, str(e)))
            exit(1)
        else:
            helper.log_debug("Succesfully parsed query results for client_id %s from o %s" % (client_id, url))
            return results   

def validate_input(helper, definition):
    api_endpoint   = definition.parameters.get('api_endpoint', None)
    get_defender_connectivity(helper, api_endpoint)
 
def collect_events(helper, ew):
    global_account = helper.get_arg('client_id', None)
    client_id = global_account.get("username", None)
    secret = global_account.get("password", None)
    tenant_id = helper.get_arg('tenant_id', None)
    api_endpoint = helper.get_arg('api_endpoint', None)
    query = helper.get_arg('query', None)

    access_token = get_defender_access_token(helper, client_id, secret, tenant_id)
    results = get_defender_query_results(helper, client_id, access_token, api_endpoint, query)
    helper.log_info("Got %d results for client_id %s from %s" % (len(results), client_id, api_endpoint))
    for result in results:
        eventJson = json.dumps(result, indent=2, sort_keys=True)
        event = helper.new_event(eventJson, time=None, host=None, index=helper.get_output_index(),
                                 source=None, sourcetype=helper.get_sourcetype(),
                                 done=True, unbroken=True)
        ew.write_event(event)

