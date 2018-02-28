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
from config import FormConfig
# import argparse
import re

templatepath = path.join(os.curdir, 'templates/')

baseurl = gethostname()

def make_app(name, 
        slug=None, 
        config=FormConfig()
        ):
    """a decorator that turns a class into a form app"""

    re.compile(r'[a-zA-Z0-9 ]*')
    if not re.matches(name)
        raise Exception('App names must be made only '
                'of spaces, and alphanumerical chars')

    if slug is None:
        slug = name.replace(' ', '_')

    approot = os.path.join(config['appsroot'], slug)

    if not os.path.isdir(approot):
        raise FileNotFoundError('app root does not '
                'exist')


    appdir = path.join(approot, slug)
    os.mkdir(appdir)

    def decorator(cls, 
            name=name,  # these default arguments are here
            # to bind objects from the current scope to the
            # decorator
            slug=slug, 
            config=config):
        """class decorator, that generates the app frontend"""
        form = FormApp(cls, name, slug, config)
        form.render()
        return cls

    return decorator
    
