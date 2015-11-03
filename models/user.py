from google.appengine.ext import ndb


class User(ndb.Model):

    email = ndb.StringProperty()

    course_keys = ndb.KeyProperty(repeated=True, kind='Course')
    project_keys = ndb.KeyProperty(repeated=True, kind='Project')

    @property
    def courses(self):
        return map(lambda k: k.get(), self.course_keys)

    @property
    def projects(self):
        return map(lambda k: k.get(), self.project_keys)

    @classmethod
    def get_from_authentication(cls, google_user):
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

    def create_project(self, project, course):
        """Create a project for a student and make student a member"""
        if project:
            # Add the student as project member
            project.add_member(self)
            # Add the project to the student
            self.project_keys.append(project.key)
            if course:
                # Add the course the project is for
                project.course = course.key
            self.put()

    def join_project(self, project):
        """Join an existing project"""
        if project:
            # Add the student as project member
            project.add_member(self)
            # Add the project to the student
            self.project_keys.append(project.key)
            self.put()

    def as_json(self, include_relationships=False):
        """Get the JSON representation of a user"""
        obj = {
            'email': self.email
        }
        if include_relationships:
            obj = {
                'courses': map(lambda x: x.as_json(), self.courses),
                'projects': map(lambda y: y.as_json(), self.projects)
            }
        return obj
