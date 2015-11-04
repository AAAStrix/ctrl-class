from google.appengine.ext import ndb


class Task(ndb.Model):

	title = ndb.StringProperty()
	completed = ndb.BooleanProperty()
		
	def as_json(self):
		obj = {
			'key': self.key.urlsafe(),
			'title': self.title
			'completed': self.completed
		}
		return obj

