import webapp2
from utils.decorators import user_required, protect_task, protect_project
from utils import render_json


class TaskHandler(webapp2.RequestHandler):

    @user_required
    @protect_task('key')
    def post(self):
        """
        Toggle completion of a task

        Takes a task, inverts the completion and saves it
        """
        task = self.params.task
        task.completed = not task.completed
        task.put()
        render_json(self, obj=task.as_json())

class TaskRemoveHandler(webapp2.RequestHandler):
        
	@user_required
	@protect_project('project_key')
	@protect_task('task_key')
	def get(self):
		task_key = self.params.task.key
		project = self.params.project
		project.remove_task(task_key)
		render_json(self)
		
