import webapp2
from utils.decorators import user_required
from utils import render_template, render_json
from models.task import Task
from models.project import Project


class TaskHandler(webapp2.RequestHandler):

    @user_required
    def post(self):
        """
        Toggle completion of a task

        Takes a task, inverts the completion and saves it
        """
        task_token = self.request.get('key')
        task = Task.find_with_key(task_token)
        task.completed = not task.completed
        task.put()
        render_json(self, obj=task.as_json())
