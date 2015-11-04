import webapp2
from utils.decorators import user_required
from utils import render_template, render_json
from models.course import Course


class CourseListHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        params = {
            'courses': self.auth.user.courses
        }
        render_template(self, 'course_list.html', params)

    @user_required
    def post(self):
        """
        Creates a new course object with some title

        Automatically adds the user to the course, and the course to the user
        """
        title = self.request.get('title')
        course = Course.new(title)
        self.auth.user.add_course(course)
        self.redirect(course.url)


class CourseHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        course_token = self.request.get('key')
        course = Course.find_with_key(course_token)
        projects = self.auth.user.projects_for_course(course)
        project_json = map(lambda p: p.as_json(include_relationships=True), projects)
        tasks = self.auth.user.tasks_for_course(course)
        task_json = map(lambda t: t.as_json(), tasks)
        params = {
            'course': course,
            'project_json': project_json,
            'course_key': course.key.urlsafe(),
            'task_json': task_json
        }
        render_template(self, 'course.html', params)


class CourseSearchHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        search = self.request.get('query')
        results = Course.find_with_partial_title(search)
        obj = {
            'courses': map(lambda x: x.as_json(), results)
        }
        render_json(self, obj=obj)


class CourseAddHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        render_template(self, 'add_courses.html')

    @user_required
    def post(self):
        course_token = self.request.get('key')
        course = Course.find_with_key(course_token)
        self.auth.user.add_course(course)
        render_json(self)
