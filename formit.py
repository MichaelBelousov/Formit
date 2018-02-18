#!/usr/bin/env python3

"""
A script for converting marked-up python backends to an HTML and php frontend.

syntax:

    '''
    all other text in the docstring is independent
    @parameter[type|format] name
    @result[type] name  # optional comments
    # maybe:
    # @result[type|format=default] name
    # @result[type|format : default] name 
    !directive arg1, arg2, etc
    '''

types:

    str
    num
    bool
    ipv4
    ipv6
    mac
    cidr
    datetime
    time
    email
    url
    table|key1,key2,key3
    datetime|format -> datetime|%Y-%M-%D:%h-%m-%s
    date|format
    time|format
    re|format -> re|/expr/
    none

directives:
    !group GROUPNAME
    !noalert

"""

# TODO: use the | syntax to delimit multiple type entries? Or have it so multiple python functions can point to the same input, with different input types!

import sys
import os
from os import path
from socket import gethostname
from secappsutils import validatorsplus as validators
import inspect
import jinja2plus as jinjaplus
from compose import FormApp
# import argparse

templatepath = path.join(os.curdir, 'templates/')

baseurl = gethostname()

def make_app(name="My App", 
        slug='my_app', 
        approot=os.curdir,
        templatepath=templatepath):
    """a decorator that turns a class into a form app"""

    if not os.path.isdir(approot):
        raise FileNotFoundError('app root does not '
                'exist')

    appdir = path.join(approot, slug)
    os.mkdir(appdir)

    def decorator(cls, 
            name=name,
            baseurl=baseurl,
            slug=slug, 
            appdir=appdir, 
            template=templatepath):
        """class decorator, that generates the app frontend"""
        form = FormApp(cls, name, baseurl, appdir, templatepath)
        form.render()
        return cls

    return decorator
    
