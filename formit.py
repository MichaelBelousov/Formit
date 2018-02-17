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
from secappsutils import validatorsplus as validators
import inspect
from jinja2plus import render
# import argparse

template_path = path.join(os.curdir, 'templates/')

def make_app(name="My App", 
        slug='my_app', 
        approot=os.curdir,
        template_path=template_path):
    """a decorator that turns a class into an app"""

    if not os.path.isdir(approot):
        raise FileNotFoundError('app root does not '
                'exist')

    appdir = path.join(approot, slug)
    os.mkdir(appdir)

    def decorator(cls):
        funcs = [f for f in dir(cls) if f not in excludes 
                and callable(getattr(cls, f))]
        # determine form inputs

        for func in funcs:
            source = func.__doc__
            for directive in pdirective.scanString(source):
                print(directive)
            for param in pparam.scanString(source):
                print(param)
            for result in presult.scanString(source):
                print(result)
        # determine 

        # didn't touch it, so return it
        return cls

    return decorator
    

def make_app(cls):
    """a decorator that turns a class into an app"""

    if not isinstance(cls, type):
        raise TypeError('Only classes can be'
                ' made into apps.')

    # soon-to-be decorated wrapper class
    class ClassWrapper(cls):
        othercls = cls
    # decoration is clearer, here
    funcs = [f for f in dir(ClassWrapper) if callable(getattr(ClassWrapper, f))]
    excludes = ('__class__',)
    for e in excludes:
        funcs.remove(e)
    for fname in funcs:
        func = getattr(ClassWrapper, fname)
        def decorated(*args, **kwargs):
            return func(*args, **kwargs)
        setattr(ClassWrapper, fname, decorated)

    # @wraps might not necessarily work so...
    ClassWrapper.__doc__ = cls.__doc__
    ClassWrapper.__name__ = cls.__name__

    return ClassWrapper

def make_named_app(name):
    # do something
    return make_app
