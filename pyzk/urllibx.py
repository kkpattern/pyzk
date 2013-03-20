# Copyright (c) 2012 zhangkai

# Util functions and classes of urllib2 module

import urllib
import urllib2


class RedirectError(Exception):
    def __init__(self, code, new_url):
        self.__code = code
        self.__new_url = new_url

    def __str__(self):
        return "Redirect to: %s" % self.__new_url

    def new_url(self):
        return self.__new_url

    def code(self):
        return self.__code

class NoRedirect(urllib2.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        raise RedirectError(code, newurl)

class URLOpener(object):
    """URLOpener: user http get and http post to open url."""
    def __init__(self, proxy=None, redirect=True):
        proxy_parameter = {}
        if proxy:
            proxy_parameter.extend({'http': proxy, 'https':proxy})
        proxy_handler = urllib2.ProxyHandler(proxy_parameter)
        if redirect:
            redirect_handler = urllib2.HTTPRedirectHandler()
        else:
            redirect_handler = NoRedirect()
        self.__url_opener = urllib2.build_opener(
                proxy_handler, redirect_handler)

    def http_get(self, url, parameters=None, headers={}):
        if parameters:
            url = url+'?'+urllib.urlencode(parameters)
        return self.open(url, data=None, headers=headers)
    
    def http_post(self, url, parameters={}, headers={}):
        parameters = urllib.urlencode(parameters)
        return self.open(url, data=parameters, headers=headers)

    def open(self, url, data=None, headers=None):
        request = urllib2.Request(url, data, headers)
        f = self.__url_opener.open(request)
        data = f.read()
        content_length = int(f.info().getheader("content-length"))
        if len(data) != content_length:
            raise IOError("Imcomplete data")
        return data
                


