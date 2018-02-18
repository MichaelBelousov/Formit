
from pyparsing import *  #use psyco for performance?
from functools import reduce
from operator import or_

ParserElement.inlineLiteralsUsing(Suppress)
# ParserElement.setDefaultWhitespaceChars(' \t')

lineBegin = Regex(r'^\s*')

# special literals
MARK = '@'
DMARK = '!'
SPACE = Suppress(White())

def raise_invalid_type():
    raise SyntaxError('Invalid Input Type')

'''
typevalidators = {'str' : lambda t: True,   # should actually use printable character checking
            'ipv4' : validators.ipv4,
            'cidr' : validators.cidr,
            'ipv6' : validators.ipv6,
            'mac' : validators.mac_address,
            'num' : 
typevalidators.setdefault(raise_invalid_type)
'''

pname = Combine(Word(alphanums) + Optional(Word(alphanums+'_-')))
pnumber = Combine(Word(nums) + Optional('.' + Word(nums)))

ptype = reduce(or_, [CaselessKeyword(x) for x in 
    ('str', 'ipv4', 'cidr', 'mac', 'num', 'table', 'datetime', 'email')])
# ptype = NoMatch() | 'str' | 'ipv4' | 'cidr' |\
                    # 'mac' | 'num' | 'table' |\
                    # 'datetime' | 'email'

# pregexformat = Combine('/' + Word(printables) + '/')

ptableformat = Group(delimitedList(pname))
pdatetimeformat = Combine(
    OneOrMore(
        Word(alphanums+'%-_:./,'),
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
            str'
            )
        + SPACE 
        + pname                     ('name')
)  #.setResultsName('param')

presult = (
        MARK 
        + Keyword('result')         ('specifier')
        + ptypedef                  ('type')
        + Optional(
            SPACE 
            + pname,
            default='result'
            )                       ('name')
)  #.setResultsName('result')

pdirective = (
        DMARK 
        + pdirective                ('specifier')
        + Optional(pdirectiveargs)  ('args')
)  #.setResultsName('directive')

pstatement= (
        (pdirective | pparam | presult)
        + Suppress(restOfLine)
        # + lineEnd
)


pstatement.ignore(pythonStyleComment)

# TODO: use this
# pdocstr = ZeroOrMore(
        # (Group(pstatement) | restOfLine)
        # + (lineEnd | stringEnd),
        # stopOn=stringEnd
# )
# pdocstr = delimitedList(Group(pstatement), lineEnd)


########## End Parser #############

from compose import Form

def param(form, parsed):
    """function for parsing param statements"""
    assert isinstance(form, Form), 'form arg must be Form instance'

    paramname = parsed['name']
    if paramname in form.inputs:
        form.inputs[parsed] = 
    form.inputs[parsed['name']] = 
    print('param', parsed)

def result(form, parsed):
    """function for parsing result statements"""
    assert isinstance(form, Form), 'form arg must be Form instance'
    print('result', parsed)

def group(form, parsed):
    """function for parsing group directives"""
    assert isinstance(form, Form), 'form arg must be Form instance'
    print('group', parsed)

def noalert(form, parsed):
    """function for parsing noalert directives"""
    assert isinstance(form, Form), 'form arg must be Form instance'
    print('noalert', parsed)

commands = {
        'param'     : param,
        'result'    : result,
        'group'     : group,
        'noalert'   : noalert
        }


