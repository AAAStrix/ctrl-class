from google.appengine.ext import ndb


class User(ndb.Model):
    email = ndb.StringProperty()
    courses = ndb.StringProperty(repeated=True)

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
        if course:
            self.courses.append(course)
            self.courses.put()
