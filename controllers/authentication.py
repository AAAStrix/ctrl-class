#!/usr/bin/env python

import webapp2
from google.appengine.api import users
from utils import render_template


class LoginHandler(webapp2.RequestHandler):

    def get(self):
        params = {
            'login_url': users.create_login_url()
        }
        render_template(self, 'login.html', params)
