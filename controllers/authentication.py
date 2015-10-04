#!/usr/bin/env python

import webapp2


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Login Handler!')


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Logout handler!')
