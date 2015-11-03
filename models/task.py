from google.appengine.ext import ndb

class Task(ndb.Model):

	title = ndb.StringProperty()
	project_keys = ndb.KeyProperty(repeated=True, kind='Project')
	
	@property
	def projects(self):
		return map(lambda k: k.get(), self.project_keys)
		
	@property
	def url(self):
		return '/task?key={}'.format(self.key.urlsafe())
		
	@classmethod
	def new(cls, title):
		new_task = cls(title=title)
		new_task.put()
		return new_task
		
	@classmethod
	def find_with_key(cls, key)
		return ndb.Key(urlsafe=key).get()
		
	def as_json(self, include_relationships=False):
		obj = {
			'key': self.key.urlsafe(),
			'title': self.title
		}
		if include_relationships:
			obj = {
				'projects' = map(lambda x: x.as_json(), self.projects)
			}
		return obj
			