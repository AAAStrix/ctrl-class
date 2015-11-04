import webapp2
from utils.decorators import user_required
from utils import render_template, render_json
from models.project import Project
from models.course import Course
from models.task import Task
from models.user import User


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
        course = Course.find_with_key(self.request.get('course_key'))
        self.auth.user.create_project(project)
        self.redirect(project.url)


class ProjectHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        project_token = self.request.get('key')
        project = Project.find_with_key(project_token)
        tasks = self.auth.user.tasks_for_project(project)
        task_json = map(lambda t: t.as_json(), tasks)
        #members = self.auth.user.
        #member_json = map(lambda m: m.as_json(), members)
        params = {
            'project': project,
            'task_json': task_json,
            #'member_json': member_json,
            'course_key': self.request.get('course_key'),
            'project_key': project.key.urlsafe(),
        }
        render_template(self, 'project.html', params)


class ProjectCreateHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        render_template(self, 'project.html')

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
        
class TaskCreateHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        render_template(self, 'project.html')

    @user_required
    def post(self):
        """
        Endpoint to create a new task

        Request Parameters:
            course_key -> NDB key for the course to add to
            title -> Title to use for the new task
        """
        
        project = Project.find_with_key(self.request.get('project_key'))
        course = Course.find_with_key(project.course)
        #course = Course.find_with_key(self.request.get('course_key'))
        #course_key = project.course.urlsafe()

        # Create the new Task object
        task_title = self.request.get('title')
        task = Task(title=task_title)

        project.add_task(task)
        task.put()
        self.redirect(project.url)

class MemberListHandler(webapp2.RequestHandler):
    @user_required
    def get(self):
        params = {
            'members': self.auth.user.members
        }
        render_template(self, 'project.html', params)

    @user_required
    def post(self):
        ''' Ugly way to do this for now, but it's operational '''
        email = self.request.get('email')
        qry = User.query(User.email == email)
        user = qry.get()
        project = Project.find_with_key(self.request.get('project_key'))
        user.add_project(project)
        project.put()
        render_json(self)
        self.redirect(project.url)
        


