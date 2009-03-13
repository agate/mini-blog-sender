import cgi
import os

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class User(db.Model):
  username = db.StringProperty(required=True)
  password = db.StringProperty(required=True)
  date = db.DateTimeProperty(auto_now_add=True)

class MiniBlog(db.Model):
  username = db.StringProperty(required=True)
  password = db.StringProperty(required=True)
  type     = db.StringProperty(required=True, choices=set(["fanfou", "douban", "jiwai"]))
  owner    = db.ReferenceProperty(User)

#class FanfouSender(Sender):
#  def send():

#class Sender():
#  def send():
#    message = self.request.get('message')
#    author = base64.b64encode('username' + ":" + 'password')

#    status = self.request.get('status')
#    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/xml", "Authorization": "Basic " + author}
#    params = urllib.urlencode({"status": status})
#    url = "http://api.fanfou.com/statuses/update.xml"
#    result = urlfetch.fetch(url, params, urlfetch.POST, headers)

class Signup(webapp.RequestHandler):
  def get(self):
    users = db.GqlQuery("SELECT * FROM User ORDER BY date DESC")

    template_values = {
      'users':users
    }

    path = os.path.join(os.path.dirname(__file__), 'signup.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):
    username = self.request.get('username')
    password = self.request.get('password')
    user = User(username=username, password=password)
    user.put()
    self.redirect('/signup')
    

class MainPage(webapp.RequestHandler):
  def get(self):
    users = db.GqlQuery("SELECT * FROM User ORDER BY date DESC")

    template_values = {
      'users':users
    }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/signup', Signup)], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
