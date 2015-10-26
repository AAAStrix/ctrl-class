from google.appengine.ext import ndb


class User(ndb.Model):

    email = ndb.StringProperty()

    course_keys = ndb.KeyProperty(repeated=True, kind='Course')

    @property
    def courses(self):
        return map(lambda k: k.get(), self.course_keys)

    @classmethod
    def get_from_authentication(self, google_user):
        """Get or create a user based on the ID retrieved from Google"""
        user_id = google_user.user_id()
        user = User.get_by_id(user_id)

        # Create the user if we couldn't find them
        if not user:
            email = google_user.nickname()
            user = User(id=user_id, email=email)
            user.put()

        return user

    def add_course(self, course):
        """Add a student to a course and vice versa"""
        if course:
            # Add the student to the course
            course.add_student(self)
            # Add the course to the student
            self.course_keys.append(course.key)
            self.put()
