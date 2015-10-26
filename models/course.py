from google.appengine.ext import ndb


class Course(ndb.Model):

    title = ndb.StringProperty()

    student_keys = ndb.KeyProperty(repeated=True, kind='User')

    @property
    def students(self):
        return map(lambda k: k.get(), self.student_keys)

    def add_student(self, user):
        self.student_keys.append(user.key)
        self.put()
