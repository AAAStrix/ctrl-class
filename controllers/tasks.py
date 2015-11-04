import webapp2
from utils.decorators import user_required
from utils import render_template, render_json
from models.task import Task
from models.project import Project	
		
class TaskHandler(webapp2.RequestHandler):
	
	@user_required
	def get(self):
		task_token = self.request.get('key')
		task = Task.find_with_key(task_token)
		
	def post(self):
		task.completed == true
		task.put()
		render_json(self)
		
		
		
		
