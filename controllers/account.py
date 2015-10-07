import webapp2
from utils.decorators import user_required


class CourseHandler(webapp2.RequestHandler):

    @user_required
    def get(self):
        self.response.write('Your courses: ' + '<br/>')
        for course in self.auth.user.courses:
            self.response.write("%s<br/>" % course)
        #(pseudo) call: for all, print/apply to gui list --> user.courses + '<br/>'

    @user_required
    def post(self):
        course = self.request.get('course')
        self.auth.user.add_course(course)
        self.redirect('/')
        #(pseudo) user.add_course(course)
