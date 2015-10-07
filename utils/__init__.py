import os
from google.appengine.ext.webapp import template


def render_template(handler, templatename, templatevalues={}):
    # Copy the original hash to avoid mutation and add the authentication
    # information to it
    values = templatevalues.copy()
    if hasattr(handler, 'auth'):
        values.update({
            'auth': handler.auth
        })

    path = os.path.join(os.path.dirname(__file__), '../views/' + templatename)
    html = template.render(path, values)
    handler.response.out.write(html)
