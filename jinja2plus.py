"""
A wrapper of the `jinja` module for some extensions and simplifications
"""


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


# XXX: might want to rid kwargs for consistency with jinja api
@add_to_jinja('render')
def render(template_path, context={}, **kwargs):
    """renders a template with a context"""
    context.update(kwargs)
    path, filename = os.path.split(template_path)
    return jinja2.Environment(
            loader=jinja2.FileSystemLoader(path or os.curdir)
            ).get_template(filename).render(context)


@add_to_jinja('renderto')
def renderto(template_path, dest=None, context={}, **kwargs):
    """renders a template with a context"""
    if os.path.isdir(dest):
        _, destfname = os.path.split(template_path)
        dest = os.path.join(dest, destfname)
    with open(dest, 'w') as f:
        res = render(template_path, context, **kwargs)
        f.write(res)
    return dest


from jinja2 import *

