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

    num
    str
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

import ast
import sys
#use psyco for performance?
from pyparsing import *
import validatorsplus as validators
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

from functools import reduce
from operator import or_
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

noalert = 'noalert'

class FormSpec(object): 
    def __init__(self, params, results, **kwargs):
        if noalert in kwargs:
            pass
        self.params = params
        self.results = results
        for p in params:
            pass
        for r in results:
            pass
    def tohtml(self):
        return ''

# NOTE: seems more convenient, but didn't work very well
# pdocstr = delimitedList(Optional(pline), Suppress(lineEnd))
# pdocstr.setParseAction(FormSpec)

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
    import secappsutils.generics as generics
    get_formspec(generics.email_results)
    import code
    code.interact(local=locals())


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
