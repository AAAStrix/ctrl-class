import webapp2
from decorators import user_required


class MainHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        self.response.write('Hello, ' + self.auth.user.nickname() + '<br />')
        self.response.write('<a href="' + self.auth.logout_url + '">Logout</a>')
