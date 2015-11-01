from google.appengine.ext import ndb
from google.appengine.api import search
from utils import tokenize_autocomplete


class Course(ndb.Model):

    title = ndb.StringProperty()

    student_keys = ndb.KeyProperty(repeated=True, kind='User')

    @property
    def students(self):
        return map(lambda k: k.get(), self.student_keys)

    @property
    def url(self):
        return '/course?key={}'.format(self.key.urlsafe())

    @classmethod
    def new(cls, title):
        """
        Factory method for creating Course objects

        Required because we need to set up the index so that we can search for
        these course objects later based on a partial title match
        """
        # Create the new course objects
        new_course = cls(title=title)
        new_course.put()

        # Update the search index
        index = search.Index(name='course_title_autocomplete')
        doc_id = new_course.key.urlsafe()
        token = ','.join(tokenize_autocomplete(title))
        document = search.Document(
            doc_id=doc_id,
            fields=[search.TextField(name='title', value=token)])
        index.put(document)

        # Return the new Course object
        return new_course

    @classmethod
    def find_with_partial_title(cls, query):
        """Find courses with a title that partially matched the query"""
        if len(query) == 0:
            return []
        r = search.Index(name='course_title_autocomplete').search('title:{}'.format(query))
        return [ndb.Key(urlsafe=m.doc_id).get() for m in r]

    @classmethod
    def find_with_key(cls, key):
        return ndb.Key(urlsafe=key).get()

    def add_student(self, user):
        """Add a student to the course"""
        self.student_keys.append(user.key)
        self.put()

    def as_json(self, include_relationships=False):
        """Get the JSON representation of a course"""
        obj = {
            'key': self.key.urlsafe(),
            'title': self.title
        }
        if include_relationships:
            obj['students'] = map(lambda x: x.as_json(), self.students)
        return obj