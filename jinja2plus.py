"""
A wrapper of the `jinja` module for some extensions and simplifications
"""

# this module is decorator heaven

import jinja2
from functools import wraps
import os

def add_to_jinja(name):
    """decorator for adding validators to this wrapper module"""
    def wrap(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        setattr(jinja2, name, wrapped)
        return wrapped
    return wrap

@add_to_jinja('render')
def render(template_path, context={}):
    """renders a template with a context"""
    path, filename = os.path.split(template_path)
    return jinja2.Environment(
            loader=jinja2.FileSystemLoader(path or os.curdir)
            ).get_template(filename).render(context)

from jinja2 import *

