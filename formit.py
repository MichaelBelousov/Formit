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
    URL
    table|key1,key2,key3
        datetime|format -> datetime|%Y-%M-%D:%h-%m-%s
        date|format
        time|format
        re|format -> re|/expr/

NAMES?:
    - formit
    - d2h?

"""

# TODO: use the | syntax to delimit multiple type entries? Or have it so multiple python functions can point to the same input, with different input types!

import sys
from secappsutils import validatorsplus as validators
from pyparsing import *  #use psyco for performance?
from functools import reduce
from operator import or_
# import argparse

ParserElement.inlineLiteralsUsing(Suppress)
#special literals
MARK = '@'
DMARK = '!'
SPACE = Suppress(White())

def raise_invalid_type():
    raise SyntaxError('Invalid Input Type')

typevalidators = {'str' : lambda t: True,   # should actually use printable character checking
            'ipv4' : validators.ipv4,
            'cidr' : validators.cidr,
            'ipv6' : validators.ipv6,
            'mac' : validators.mac_address,
            'num' : validators.number}
typevalidators.setdefault(raise_invalid_type)

pname = Combine(Word(alphanums) + Optional(Word(alphanums+'_-')))
pnumber = Combine(Word(nums) + Optional('.' + Word(nums)))
pcomment = '#' + restOfLine()

ptype = reduce(or_, [CaselessKeyword(x) for x in 
    ('str', 'ipv4', 'cidr', 'mac', 'num', 'table', 'datetime', 'email')])
# ptype = NoMatch() | 'str' | 'ipv4' | 'cidr' |\
                    # 'mac' | 'num' | 'table' |\
                    # 'datetime' | 'email'

pregexformat = Combine('/' + Word(printables) + '/')

ptableformat = Group(delimitedList(pname))
pdatetimeformat = Combine(
    OneOrMore(
        Word(alphanums+'%-_:./'),
        stopOn=']'),
    adjacent=False,
    joinString=' '
    )

pformat = ptableformat | pdatetimeformat

ptypedef = (
        '[' 
        + ptype                     ('type')
        + Optional(
            '|' 
            + pformat,
            default='')             ('format')
        + ']'
)

pdirective = pname
pdirectiveargs = delimitedList(Word(alphanums))

pparam = (
        MARK 
        + Keyword('param')          ('specifier')
        + Optional(
            ptypedef                ('type'),
            default='str'
            )
        + SPACE 
        + pname                     ('name')
)

presult = (
        MARK 
        + Keyword('result')         ('specifier')
        + ptypedef                  ('type')
        + Optional(
            SPACE 
            + pname,
            default='result'
            )                       ('name')
)

pdirective = (
        DMARK 
        + pdirective                ('specifier')
        + Optional(pdirectiveargs)  ('args')
)

pline = pparam | presult | pdirective
pline.ignore(pcomment)


########## end parsing stuff #############

# NOTE: seems more convenient, but didn't work very well
# pdocstr = delimitedList(Optional(pline), Suppress(lineEnd))
# pdocstr.setParseAction(FormSpec)

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
    for name in funcs:
        func = getattr(ClassWrapper, name)
        print(func.__doc__)
        def decorated(*args, **kwargs):
            print('hello')
            return func(*args, **kwargs)
        setattr(ClassWrapper, name, decorated)

    # @wraps might not necessarily work so...
    ClassWrapper.__doc__ = cls.__doc__
    ClassWrapper.__name__ = cls.__name__

    return ClassWrapper

def make_named_app(name):
    # do something
    return make_app

def example(title, root):
    """
    # example
    !noalert
    @param[str] title
    @param[ipv4] root
    @result[table|key1, key2, key3]

    this function is an example for the form declaration syntax
    """
    pass

def get_formspec(obj):
    """returns form specification of the function object"""
    source = obj.__doc__

    directives = [t[0] for t in pdirective.scanString(source)]
    params = [t[0] for t in pparam.scanString(source)]
    results = [t[0] for t in presult.scanString(source)]
    form = FormSpec(params, results, **{k[0]:(k[1] if len(k)>1 else None) for k in directives})
    return form


if __name__ == '__main__':
    '''
    target = sys.argv[1]
    print(target)
    contents = None
    with open(target) as fd:
        contents = fd.read()
    module = ast.parse(contents)
    moddoc = ast.get_docstring(module)

    funcs = [n for n in module.body if isinstance(n, ast.FunctionDef)]
    classdefs = [n for n in module.body if isinstance(n, ast.ClassDef)]
    for classdef in classdefs:
        methods = [f for f in classdef.body 
                if isinstance(n, ast.FunctionDef)]
        for method in methods:
            docstr = ast.get_docstring(method)
            getspec()
    '''

