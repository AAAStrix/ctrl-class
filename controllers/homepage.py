import webapp2
from utils.decorators import user_required
from utils import render_template


class MainHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        render_template(self, 'home.html')
