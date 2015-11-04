import webapp2
from utils.decorators import user_required
from google.appengine.api import mail
from utils import render_template


class MainHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        project_json = map(lambda x: x.as_json(), self.auth.user.projects)
        params = {
            'courses': self.auth.user.courses,
            'project_json': project_json
        }
        render_template(self, 'home.html', params)

    @user_required
    def post(self):
        from_address = 'contact@ctrl-class.appspotmail.com'
        subject = 'Contact from ctrl-class'
        body = 'Welcome to ctrl-class! Take control over your courses and projects.\n\
                 Questions? Contact us at contact@ctrl-class.appspotmail.com. \n\n\
                 -The ctrl-class team'
        mail.send_mail(from_address, self.auth.user.email, subject, body)
