import webapp2

class CourseHandler(webapp2.RequestHandler):

	def get(self):
		self.response.write('Your courses: ' + '<br/>')
		for course in self.auth.user.courses
			self.response.write("%s<br/>" % course)
		#(pseudo) call: for all, print/apply to gui list --> user.courses + '<br/>'

	def post(self):
		course = self.request.get('course')
		self.auth.user.add_course(course)
		#(pseudo) user.add_course(course)