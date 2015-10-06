#!/usr/bin/env python

import webapp2
from google.appengine.api import users


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        login_url = users.create_login_url()
        self.response.write('<a href="' + login_url + '">Log in!</a>')