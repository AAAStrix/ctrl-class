from google.appengine.ext import ndb


class User(ndb.Model):
    user_id = ndb.StringProperty()
    email = ndb.StringProperty()

    @classmethod
    def get_from_authentication(self, google_user):
        """Get or create a user based on the ID retrieved from Google"""
        user_id = google_user.user_id()
        user = User.get_by_id(user_id)

        # Create the user if we couldn't find them
        if not user:
            email = google_user.nickname()
            user = User(user_id=user_id, email=email, id=user_id)
            user.put()

        return user
