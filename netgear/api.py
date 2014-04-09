# -*- coding: utf-8 -*-
import json
import urllib
import urllib2
import cookielib
import Cookie
import StringIO
from urlparse import urljoin
from .poster.encode import multipart_encode
from .poster.streaminghttp import register_openers

class Api(object):

    _app_password = ''
    _app_host     = ''
 
    def __init__(self, app_password='', app_host='', debug=False):
        """ Construct an Api object, 
            taking an APP PASSWORD and API URL parameter """
        self._app_password = app_password
        self._app_host     = app_host
        self._debug        = debug
        self._cookies      = cookielib.CookieJar()
        self._opener       = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cookies))

    def sendRequest(self, path, params=None, headers=None):
        """ Send the request to the API server
            also encrypts the request, then checks
            if the results are valid """
        if self._debug: print "Request Params: %s" % params
        url     = urljoin(self._app_host, path)
        request = urllib2.Request(url)
        self._cookies.add_cookie_header(request)
        if self._debug: print "Querying '%s'..." % url
        if params:
            return self._opener.open(request, urllib.urlencode(params), headers).read()
        else:
            return self._opener.open(request).read()
 
    def login(self):
        res = self.sendRequest('/base/netgear_login.html', {
          'pwd': self._app_password
        })
        return ('logout' in res)

    def downloadConfig(self):
        """ Retrieve the switch configuration """
        res = self.sendRequest('/filesystem/startup-config')
        return res

    def uploadConfig(self, configfile):
        """ Send configuration to the switch """
        if not self.login(): raise Exception('Login Failed')
        elif self._debug: print 'Successfully logged in'
        register_openers()
        datagen, headers = multipart_encode({
            'v_1_10_2'          : 'Text Configuration',
            '.v_1_3_1_handle'   : open(configfile, 'rb'),
            'v_1_3_2'           : 'not in progress',
            'v_1_9_1'           : 'image1',
            'v_1_9_2'           : 1,
            'v_1_9_3'           : 'Enable',
            'v_1_20_1'          : '',
            'v_1_200_1'         : '',
            'v_2_3_1'           : 'not in progress',
            'v_2_4_1'           : 'None',
            'v_6_2_1'           : 'Enable',
            'submit_flag'       : 8,
            'submit_target'     : 'http_file_download.html',
            'err_flag'          : 0,
            'err_msg'           : '',
            'clazz_information' : 'http_file_download.html',
            'v_1_5_1'           : 'APPLY'
        })
        res = self.sendRequest('/http_file_download.html/a1', datagen, headers)
        return ('File transfer operation completed' in res)

def encrypt(key, plaintext):
    padded_key = key.ljust(KEY_SIZE, '\0')
    padded_text = plaintext + (BLOCK_SIZE - len(plaintext) % BLOCK_SIZE) * '\0'
    r = rijndael.rijndael(padded_key, BLOCK_SIZE)
    ciphertext = ''
    for start in range(0, len(padded_text), BLOCK_SIZE):
        ciphertext += r.encrypt(padded_text[start:start+BLOCK_SIZE])
    encoded = base64.b64encode(ciphertext)
    return encoded

def decrypt(key, encoded):
    padded_key = key.ljust(KEY_SIZE, '\0')
    ciphertext = base64.b64decode(encoded)
    r = rijndael.rijndael(padded_key, BLOCK_SIZE)
    padded_text = ''
    for start in range(0, len(ciphertext), BLOCK_SIZE):
        padded_text += r.decrypt(ciphertext[start:start+BLOCK_SIZE])
    plaintext = padded_text.split('\x00', 1)[0]
    return plaintext




