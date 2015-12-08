import webapp2
from utils.decorators import user_required, protect_project, protect_course
from utils import render_template, render_json
from models.project import Project
from models.task import Task
from models.user import User


class ProjectListHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        params = {
            'projects': self.auth.user.projects
        }
        render_template(self, 'project_list.html', params)


class ProjectHandler(webapp2.RequestHandler):

    @user_required
    @protect_project('key')
    def get(self):
        project = self.params.project
        task_json = map(lambda t: t.as_json(), project.tasks)
        params = {
            'project': project,
            'task_json': task_json,
            'course_key': self.request.get('course_key'),
            'project_key': project.key.urlsafe(),
        }
        render_template(self, 'project.html', params)


class ProjectCreateHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        render_template(self, 'project.html')

    @user_required
    @protect_course('course_key')
    def post(self):
        """
        Endpoint to create a new project

        Request Parameters:
            course_key -> NDB key for the course to add to
            title -> Title to use for the new project
        """
        course = self.params.course

        # Create the new Project object
        project_title = self.request.get('title')
        project = Project(title=project_title, course_key=course.key)

        self.auth.user.add_project(project)
        self.redirect(course.url)


class TaskCreateHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        render_template(self, 'project.html')

    @user_required
    @protect_project('project_key')
    def post(self):
        """
        Endpoint to create a new task

        Request Parameters:
            project_key -> NDB key for the project to add to
            title -> Title to use for the new task
			date -> Due Date to associate with new task
        """
        project = self.params.project

        # Create the new Task object
        task_title = self.request.get('title')
	task_duedate = self.request.get('date')
        task = Task(title=task_title, completed=False, dueDate=task_duedate)
        task_key = task.put()

        project.add_task(task_key)
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
        # Get the user to invite
        email = self.request.get('email')
        qry = User.query(User.email == email)
        user = qry.get()

        # TODO: Do something to handle the email being invalid

        # Get the project to add to
        project = Project.find_with_key(self.request.get('project_key'))

        # Ensure that the user is in the course for that project
        course = project.course
        if course in user.courses:
            user.add_project(project)
            project.put()
            render_json(self)
            self.redirect(project.url)
        else:
            # Do something to handle the error
            render_template(self, 'not_found.html')
