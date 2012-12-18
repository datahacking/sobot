#!/usr/bin/env python
#-*-coding: utf-8 -*-

import json
import os
import urllib
import urllib2
import logging
import webapp2
import jinja2

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from secrets import RenrenKey
from renren import Renren
import weibo

from short import GoogleURLShort

jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

class MessageDB(ndb.Model):
    """Models an reddit entry with id and date."""
    reddit_id = ndb.StringProperty()
    status = ndb.TextProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)


def get_access_token():
    params = '&'.join(['%s=%s' % (k, v)for (k, v) in RenrenKey.iteritems()])
    request_url = 'https://graph.renren.com/oauth/token?grant_type=refresh_token&'+params
    response = urlfetch.fetch(url = request_url)
    logging.info(response.content)
    return json.loads(response.content)['access_token']

class FrontHandler(webapp2.RequestHandler):
    def get(self):
        message_query = MessageDB.query().order(-MessageDB.created_at)
        messages = message_query.fetch(20)
        
        template_values = {
            'messages': messages,
            }
        template = jinja_environment.get_template('home.html')
        self.response.out.write(template.render(template_values))
    
class Bot(webapp2.RequestHandler):
    access_token = get_access_token()

    def get(self):
        bot = Renren()
        weibo.login(weibo.USERNAME, weibo.PASSWORD)
        url = 'http://www.reddit.com/r/MachineLearning/.json'
        request = urllib2.Request(url)
        opener = urllib2.build_opener()
        request.add_header('User-Agent', 'Google App engine tutorial bot by /u/stephenlee10')
        jsondata = json.loads(opener.open(request).read())


        tweets = ''
        if 'data' in jsondata and 'children' in jsondata['data']:
            posts = jsondata['data']['children']
            posts.reverse()
            for index, post in enumerate(posts):
                entry = post['data']
                print entry['permalink'] + ' ' + entry['url']
                postid = entry['id']
                num_comments = entry['num_comments']
                
                qry = MessageDB.query(MessageDB.reddit_id==postid)
                res = qry.fetch(1)
                
                if len(res) == 0 and num_comments > 3:
                    title = entry['title']
                    score = entry['score']
                    downs = entry['downs']
                    ups = entry['ups']
                    permalink = GoogleURLShort('http://www.reddit.com' + entry['permalink']).shorten()
                    url = GoogleURLShort(entry['url']).shorten()
                    author = 'http://www.reddit.com/user/' + entry['author']
                    status = ' %s [article:%s by:%s comments:%d score:%d]' % (url, permalink, author, num_comments, score)
                    status = title + status
                    status = status.encode('utf-8')
                    logging.info(status)
                    # update weibo status
                    weibo.update_status(status)
                    #update renren status
                    bot.update_status(self.access_token, status)
                    item = MessageDB()
                    item.populate(reddit_id = postid, status = status)
                    item.put()
                    tweets += '<p>' + status + '</p>'
        logging.info(tweets)
        self.response.out.write("Done!\n" + tweets)

app = webapp2.WSGIApplication([
	('/', FrontHandler),
    ('/cron', Bot),
], debug=True)


        


    
