
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
            'num' : validators.number}
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
            default='str'
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

def param(parsed):
    print(parsed)

def result(parsed):
    print(parsed)

def group(parsed):
    print(parsed)

def noalert(parsed):
    print(parsed)

commands = {
        'param'     : param,
        'result'    : result,
        'group'     : group,
        'noalert'   : noalert
        }

########## End Commands#############

from compose import Form

def parse_docstr(obj):
    form = Form()
    source = obj.__doc__
    lines = source.split('\n')

    for ln in lines:
        data = pstatement.parseString(ln)
        if data:
            command = data[0]
            args = data[1:]
            form = commands[command](args)


