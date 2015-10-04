from google.appengine.api import users


class Authentication(object):

    user = None
    """Store the user that is currently logged in"""

    logout_url = None
    """Store the logout URL"""

    def __init__(self, user):
        self.user = user
        self.logout_url = users.create_logout_url('/login')


def user_required(handler):
    """
    Ensures that a user is logged in before allowing entrance

    If the user is logged in, it will set `self.user` to the current user
    object
    """

    def check_login(self, *args, **kwargs):
        user = users.get_current_user()

        if not user:
            try:
                self.redirect('/login', abort=True)
            except (AttributeError, KeyError):
                self.abort(403)
        else:
            self.auth = Authentication(user)
            return handler(self, *args, **kwargs)

    return check_login
