import webapp2
from utils.decorators import user_required
from utils import render_template
from models.course import Course


class CourseHandler(webapp2.RequestHandler):

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
        course = Course(title=title)
        self.auth.user.add_course(course)
        self.redirect('/courses')


class CourseSearchHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        self.response.write("course")


class CourseAddHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        render_template(self, 'add_courses.html')
