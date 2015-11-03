import webapp2
from utils.decorators import user_required
from utils import render_template, render_json
from models.task import Task
from models.project import Project	

class TaskListHandler(webapp2.RequestHandler):

	@user_required
	def get(self):
		params = {
			'tasks': self.auth.user.tasks
		}
		render_template(self, 'task_list.html', params)
		
	@user_required
	def post(self):
		title = self.request.get('title')
		project = self.request.get('project')
		project_key = Task.get_project_by_name(project)
		task = Task.new(title, project_key)
		self.auth.user.create_task(task)
		self.redirect(task.url)
		
class TaskHandler(webapp2.RequestHandler):
	
	@user_required
	def get(self)
		task_token = self.request.get('key')
		task = Task.find_with_key(task_token)
		params = {
			'task': task
		}
		render_template(self, 'task.html', params)
		
class TaskCreateHandler(webapp2.RequestHandler)
	
	@user_required
	def get(self):
		render_template(self, 'add_task.html
		
	def post(self):
		task_token = self.request.get('key')
		task = Task.find_with_key(task_token)
		project_key = Task.get_project_by_name(project)
		self.auth.user.create_task(task, project_key)
		render_json(self)
		
		
		