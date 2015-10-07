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
import os   # needs to go with render_template
import webapp2

# Import template functionality
from google.appengine.ext.webapp import template

# Import Controllers
from controllers.authentication import LoginHandler
from controllers.homepage import MainHandler

# would like to have this in a separate file for use by all handlers
def render_template(self, handler, templatename, templatevalues):
    path = os.path.join(os.path.dirname(__file__), 'views/' + templatename)
    html = template.render(path, templatevalues)
    handler.response.out.write(html) 
     
# Map Routes
routes = [
    ('/', MainHandler),
    ('/login', LoginHandler)
]

app = webapp2.WSGIApplication(routes, debug=True)
