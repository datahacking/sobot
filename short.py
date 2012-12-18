#!/usr/bin/env python

import urllib
import urllib2
import json

# shorten url using Google shorten url service
user_agent = 'User-Agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11'
api_url = 'https://www.googleapis.com/urlshortener/v1/url'

class GoogleURLShort(object):
    def __init__(self, url):
        self.url = url
        
    def shorten(self, response_all = False):
        headers = {'User-Agent': user_agent , 'Content-Type': 'application/json'}
        params = {'longUrl': self.url}
#        data = urllib.urlencode(params)
        data = json.dumps(params)
        try:
            req = urllib2.Request(api_url, data, headers)
            res = urllib2.urlopen(req)
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request'
                print 'Error code: ', e.code
                
        json_data = res.read()
        if response_all == True:
            return json_data
        else:
            return json.loads(json_data)['id']

    def expand(self, response_all=False):
        res = urllib.urlopen(api_url+'?shortUrl={0}'.format(self.url))
        json_data = res.read()
        
        if response_all == True:
            return json_data
        else:
            return json.loads(json_data)['longUrl']

# test
def test():
    url = 'http://www.google.com'
    short_url =  GoogleURLShort(url).shorten()
    print short_url
    long_url = GoogleURLShort(short_url).expand()
    print long_url

if __name__ == '__main__':
    test()


            
            

        
