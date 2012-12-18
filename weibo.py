#!/usr/bin/env python
#-*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import logging

USERNAME = 'Your weibo username'
PASSWORD = 'Your weibo password'

cookiejar = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cookiejar)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

def login(user, password):
    url = 'https://m.weibo.cn/login'
    postdata = {
        'uname': user,
        'pwd': password,
        'check': 1,
        'autoLogin': 1
        }
    payload = urllib.urlencode(postdata)
    # forge iphone headers
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language':  'en-us,en;q=0.5',
        'Connection': 'keep-alive',
        'Host':	'm.weibo.cn',
        'Referer': 'https://m.weibo.cn/login?ns=1&backURL=http%3A%2F%2Fm.weibo.cn%2F&backTitle=%D0%C2%C0%CB%CE%A2%B2%A9&vt=4',
        'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; en) AppleWebKit/534.46.0 (KHTML, like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.'      }

    cookiejar = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cookiejar)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    
    req = urllib2.Request(
        url = url,
        data = payload,
        headers = headers
        )
    try:
        response = urllib2.urlopen(req)
        text = response.read()
        logging.info(text)
    except urllib2.HTTPError, e:
        logging.info(e.code)
        logging.info('login weibo error.')
    except urllib2.URLError, e:
        logging.info(e.args)
        logging.info('login weibo error.')

def update_status(status):
    url = 'http://m.weibo.cn/mblogDeal/addAMblog?uid=2672318191&st=edfb&'
    data = {'content': status.encode('utf-8')}
    payload = urllib.urlencode(data)
    headers = {
        'Referer': 'http://m.weibo.cn/u/2672318191',
        'User-Agent': 
            'Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; en) AppleWebKit/534.46.0 (KHTML, like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.',
        'X-Requested-With': 'XMLHttpRequest'
        }
    req = urllib2.Request(
        url = url,
        data = payload,
        headers = headers
        )
    try:
        res  = urllib2.urlopen(req)
        text = res.read()
        logging.info(text)
    except urllib2.HTTPError, e:
        logging.info(e.code)
        logging.info('update weibo status error')
    except urllib2.URLError, e:
        logging.info(e.args)
        logging.info('update weibo status error')





