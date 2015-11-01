import os
import json
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


def render_json(handler, status=200, obj={}):
    handler.response.status = status
    handler.response.out.write(json.dumps(obj))


def tokenize_autocomplete(phrase):
    a = []
    for word in phrase.split():
        j = 1
        while True:
            for i in range(len(word) - j + 1):
                a.append(word[i:i + j])
            if j == len(word):
                break
            j += 1
    return a
