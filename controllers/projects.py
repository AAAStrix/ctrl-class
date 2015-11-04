import webapp2
from utils.decorators import user_required
from utils import render_template, render_json
from models.project import Project
from models.course import Course
from models.task import Task


class ProjectListHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        params = {
            'projects': self.auth.user.projects
        }
        render_template(self, 'project_list.html', params)

    @user_required
    def post(self):
        """
        Creates a new project object with some title

        Automatically adds the user as a member of the project and proj. to the user

        Adds reference to course it belongs to
        """
        title = self.request.get('title')
        course = self.request.get('course')
        course_key = Project.get_course_by_name(course) # needs implementing
        project = Project.new(title, course_key)
        self.auth.user.create_project(project)
        self.redirect(project.url)


class ProjectHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        project_token = self.request.get('key')
        project = Project.find_with_key(project_token)
        params = {
            'project': project
        }
        render_template(self, 'project.html', params)

class ProjectCreateHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        render_template(self, 'add_project.html')

    @user_required
    def post(self):
        """
        Endpoint to create a new project

        Request Parameters:
            course_key -> NDB key for the course to add to
            title -> Title to use for the new project
        """
        # Fetch the course object to add the project to
        course = Course.find_with_key(self.request.get('course_key'))

        # Create the new Project object
        project_title = self.request.get('title')
        project = Project(title=project_title, course=course.key)

        self.auth.user.add_project(project)
        project.put()
        self.redirect(course.url)

class MemberListHandler(webapp2.RequestHandler):
    @user_required
    def get(self):
        params = {
            'members': self.auth.user.members
        }
        render_template(self, 'members.html', params)

    @user_required
    def post(self):
        email = self.get.request('email')
        qry = User.query(User.email == email)
        project = Project.find_with_key(project_token)
        qry.join_project(project)
        render_json(self)

