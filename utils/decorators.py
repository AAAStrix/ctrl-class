from google.appengine.api import users
from models.user import User
from models.project import Project
from models.course import Course
from models.task import Task
from utils import render_template


class Params(object):

    def __init__(self):
        self.course = None
        self.project = None
        self.task = None

    @classmethod
    def verify_attribute(cls, handler):
        try:
            params = handler.params
        except AttributeError:
            handler.params = Params()


class Authentication(object):

    user = None
    """Store the user that is currently logged in"""

    logout_url = None
    """Store the logout URL"""

    def __init__(self, user_from_auth):
        self.user = User.get_from_authentication(user_from_auth)
        self.logout_url = users.create_logout_url('/login')


def user_required(handler):
    """
    Ensures that a user is logged in before allowing entrance

    If the user is logged in, it will set `self.auth` to an Authentication
    object.  This contains the currently logged in user and the URL for
    logging out
    """

    def check_login(self, *args, **kwargs):
        user = users.get_current_user()

        if not user:
            try:
                self.redirect('/login', abort=True)
            except (AttributeError, KeyError):
                self.abort(403)
        else:
            self.auth = Authentication(user)
            return handler(self, *args, **kwargs)

    return check_login


def protect_project(param_name):
    """
    Ensures that the user has access to the project specified by the ID in the
    query parameter
    """

    def wrap_handler(handler):

        def check_permissions(self, *args, **kwargs):
            project_token = self.request.get(param_name)
            project = Project.find_with_key(project_token)
            if project in self.auth.user.projects:
                Params.verify_attribute(self)
                self.params.project = project
                return handler(self, *args, **kwargs)
            else:
                render_template(self, 'not_found.html')

        return check_permissions

    return wrap_handler


def protect_course(param_name):
    """
    Ensures that the user has access to the course specified by the ID in the
    query parameter
    """
    def wrap_handler(handler):

        def check_permissions(self, *args, **kwargs):
            course_token = self.request.get(param_name)
            course = Course.find_with_key(course_token)
            if course in self.auth.user.courses:
                Params.verify_attribute(self)
                self.params.course = course
                return handler(self, *args, **kwargs)
            else:
                render_template(self, 'not_found.html')

        return check_permissions

    return wrap_handler


def protect_task(param_name):
    """
    Ensures that the user has access to the task specified by the ID in the
    query parameter
    """
    def wrap_handler(handler):

        def check_permissions(self, *args, **kwargs):
            task_token = self.request.get(param_name)
            task = Task.find_with_key(task_token)
            if task in self.auth.users.tasks:
                Params.verify_attribute(self)
                self.params.task = task
                return handler(self, *args, **kwargs)
            else:
                render_template(self, 'not_found.html')

        return check_permissions

    return wrap_handler
