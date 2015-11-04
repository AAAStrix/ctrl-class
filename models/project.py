from google.appengine.ext import ndb


class Project(ndb.Model):

    title = ndb.StringProperty()
    member_keys = ndb.KeyProperty(repeated=True, kind='User')
    task_keys = ndb.KeyProperty(repeated=True, kind='Task')
    course = ndb.KeyProperty()

    @property
    def members(self):
        return map(lambda k: k.get(), self.member_keys)

    @property
    def tasks(self):
        return map(lambda k: k.get(), self.task_keys)

    @property
    def url(self):
        return '/project?key={}'.format(self.key.urlsafe())

    def add_member(self, user):
        """Add a member to the project group"""
        self.member_keys.append(user.key)
        self.put()

    def add_task(self, task):
        """Add task to the project"""
        self.task_keys.append(task.key)
        self.put()

    def as_json(self, include_relationships=False):
        """
        Get the JSON representation of a project

        Note: It seems weird, but we need to include a "tasks" property in the
        JSON even if we're not including the relationship because the front-end
        code expects that property to be there for rendering purposes
        """
        obj = {
            'key': self.key.urlsafe(),
            'title': str(self.title),
            'tasks': []
        }
        if include_relationships:
            obj['course'] = self.course
            # obj['members'] = map(lambda x: x.as_json(), self.members),
            # obj['tasks'] = map(lambda y: y.as_json(), self.tasks)
        return obj

    @classmethod
    def find_with_key(cls, key):
        return ndb.Key(urlsafe=key).get()

    # def get_course_by_name(title):
        # (todo) check name against self.auth.user.courses
        # (todo) update course key from key
