import logging
import webapp2
from decorators.user_required import user_required


class MainHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        logging.info(self.auth.user)
        self.response.write('Hello, ' + self.auth.user.nickname() + '<br />')
        self.response.write('<a href="' + self.auth.logout_url + '">Logout</a>')
