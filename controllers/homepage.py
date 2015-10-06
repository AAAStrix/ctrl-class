import webapp2
from decorators import user_required


class MainHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        self.response.write('Hello, ' + self.auth.user.email + '<br />')
        self.response.write('<a href="%s">Logout</a>' % self.auth.logout_url)
		self.response.write('<br/><br/><a href="%s">My Courses</a>' % self.redirect("/courses"))