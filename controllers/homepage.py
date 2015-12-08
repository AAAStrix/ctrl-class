import webapp2
from utils.decorators import user_required
from utils import render_template


class MainHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        project_json = map(lambda x: x.as_json(include_relationships=True), self.auth.user.projects)
        task_json = map(lambda x: x.as_json(), self.auth.user.tasks);
        params = {
            'courses': self.auth.user.courses,
            'project_json': project_json,
            'task_json': task_json
        }
        render_template(self, 'home.html', params)

class AboutHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        project_json = map(lambda x: x.as_json(include_relationships=True), self.auth.user.projects)
        task_json = map(lambda x: x.as_json(), self.auth.user.tasks);
        params = {
            'courses': self.auth.user.courses,
            'project_json': project_json,
            'task_json': task_json
        }
        render_template(self, 'About.html', params)