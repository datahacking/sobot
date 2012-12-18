#-*-coding: utf-8 -*-
from google.appengine.api import urlfetch

from secrets import RenrenKey

import time
import hashlib
import logging
import urllib

class Renren(object):
    # base url
    BASE_URL = 'http://api.renren.com/restserver.do'
    def update_status(self, access_token, status, method='status.set', v='1.0', format='json'):
        call_id = str(int(time.time()*1000))
        params = {
            'access_token': access_token,
            'v': v,
            'method': method,
            'call_id': call_id,
            'format': format,
            'status': status
            }
        sig = self.get_sig(params)
        params.update({'sig': sig})
        payload = urllib.urlencode(params)
        result = urlfetch.fetch(url=self.BASE_URL,
                                payload=payload,
                                method=urlfetch.POST,
                                headers={'Content-Type': 'application/x-www-form-urlencoded'})
        logging.info(result.status_code)

    def unicode_encode(self, str):
        return isinstance(str,unicode) and str.encode('utf-8') or str
    
    def get_sig(self, params):
        message =''.join(['%s=%s' % (self.unicode_encode(k),self.unicode_encode(v)) for (k,v) in sorted(params.iteritems())])
        m=hashlib.md5(message+RenrenKey['client_secret'])
        sig=m.hexdigest()
        return sig


        
    
