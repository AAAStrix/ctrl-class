from google.appengine.ext import ndb
from google.appengine.api import search
from google.appengine.api import memcache
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

        #Delete courses
        memcache.delete('courses')
        
        # Add to memcache
        memcache.set(new_course.key.urlsafe(), new_course, namespace='course')

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
        r = search.Index(name='course_title_autocomplete').search(
            'title:{}'.format(query))
        models = [ndb.Key(urlsafe=m.doc_id).get() for m in r]
        return [item for item in models if item is not None]

    @classmethod
    def find_with_key(cls, key):
        result = memcache.get(key, namespace='course')
        if not result:
           result = ndb.Key(urlsafe=key).get()
        return result
        
    def add_student(self, user):
        """Add a student to the course"""
        self.student_keys.append(user.key)
        self.put()

    def remove_student(self, user):
        # Remove user from course projects
        for project in user.projects_for_course(self):
            project.remove_member(user)

        # Remove the user from the course
        self.student_keys.remove(user.key)
        self.put()

        # Remove the course form the user
        user.course_keys.remove(self.key)
        user.put();

    def as_json(self, include_relationships=False):
        """Get the JSON representation of a course"""
        obj = {
            'key': self.key.urlsafe(),
            'title': self.title
        }
        if include_relationships:
            obj['students'] = map(lambda x: x.as_json(), self.students)
        return obj
