#!/usr/bin/env python3

"""
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
        slug=None, 
        approot=os.curdir,
        templatepath=templatepath):
    """a decorator that turns a class into a form app"""

    if not os.path.isdir(approot):
        raise FileNotFoundError('app root does not '
                'exist')

    if slug is None:
        slug = name
        for spacechar in (' ', '\t', '\n'):
            slug = slug.replace(spacechar, '_')

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
    
