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

    def add_course(self, course):
        """Add a student to a course and vice versa"""
        if course:
            # Add the student to the course
            course.add_student(self)
            # Add the course to the student
            self.course_keys.append(course.key)
            self.put()

    def projects_for_course(self, course):
        """
        Return a list of just the projects that belong to some course

        Note: Inefficient implementation.  Instead of using a query to look up
        just the projects that match the course, we take a list of all of the
        projects that this user belongs to and then just check if the project
        belongs to the specified course

        The array comprehension belong might look kind of complicated.  In
        essence, it does the following on one line:

            matching_projects = []
            for p in self.projects:
                if p.course = c_key:
                    matching_projects.append(p)

        Using array comprehension is a much more Python-y way of doing the
        above.
        """
        c_key = course.key
        matching_projects = [p for p in self.projects if p.course == c_key]
        return matching_projects

    def tasks_for_project(self, project):
        """
        Return a list of just the tasks that belong to some project

        Using projects_for_course as template
        """
        p_key = project.key
        matching_tasks = [t for t in project.tasks if p.project == p_key]
        return matching_tasks


    def add_project(self, project):
        """
        Create a project for a student and make student a member

        Arguments:
            project: -> Project Model object
            course: -> Course Key to add to project
        """
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
                #do we need to iterate through tasks here?
            }
        return obj

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
