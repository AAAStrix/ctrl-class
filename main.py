#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

# Import Controllers
from controllers.authentication import LoginHandler
from controllers.homepage import MainHandler, AboutHandler
from controllers.courses import CourseListHandler, CourseHandler, \
    CourseAddHandler, CourseRemoveHandler, CourseSearchHandler
from controllers.projects import ProjectListHandler, ProjectHandler, \
    ProjectCreateHandler, ProjectRemoveHandler, TaskCreateHandler, \
    MemberListHandler
from controllers.tasks import TaskHandler, TaskRemoveHandler

# Map Routes
routes = [
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/about', AboutHandler),
    ('/courses', CourseListHandler),
    ('/course', CourseHandler),
    ('/courses/add', CourseAddHandler),
    ('/courses/remove', CourseRemoveHandler),
    ('/courses/search', CourseSearchHandler),
    ('/projects', ProjectListHandler),
    ('/project', ProjectHandler),
    ('/projects/add', ProjectCreateHandler),
    ('/projects/remove', ProjectRemoveHandler),
    ('/project/add_task', TaskCreateHandler),
    ('/project/members', MemberListHandler),
    ('/task/toggle', TaskHandler),
	('/task/remove', TaskRemoveHandler)
]

app = webapp2.WSGIApplication(routes, debug=True)
