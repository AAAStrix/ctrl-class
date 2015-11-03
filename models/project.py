from google.appengine.ext import ndb


class Project(ndb.Model):

    title = ndb.StringProperty()
    member_keys = ndb.KeyProperty(repeated=True, kind='User')
    task_keys = ndb.KeyProperty(repeated=True, kind='Task')
    course = ndb.KeyProperty()

    @property
    def members(self):
        return map(lambda k: k.get(), self.member_keys)
        
    def tasks(self):
        return map(lambda k: k.get(), self.task_keys)
        
    @property
    def url(self):
        return '/project?key={}'.format(self.key.urlsafe())
        
    @classmethod
    def new(cls, title):
        """
        Factory method for creating Project objects
        """
        # Create the new course objects
        new_project = cls(title=title)
        new_project.put()

        # Return the new Project object
        return new_project

    @classmethod
    def find_with_key(cls, key):
        return ndb.Key(urlsafe=key).get()
        
    def get_course_by_name(title) 
        # (todo) check name against self.auth.user.courses 
        # (todo) update course key from key

    def add_member(self, user):
        """Add a member to the project group"""
        self.student_keys.append(user.key)
        self.put()
    
    def add_task(self, task)
        """Add task to the project"""
        self.task_keys.append(task.key)
        self.put()

    def as_json(self, include_relationships=False):
        """Get the JSON representation of a project"""
        obj = {
            'key': self.key.urlsafe(),
            'title': self.title
        }
        if include_relationships:
            obj = {
                'course' = self.course
                'members' = map(lambda x: x.as_json(), self.members)
                'tasks' = map(lambda y: y.as_json(), self.tasks)
            }
        return obj
