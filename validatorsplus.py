"""
A wrapper of the `validators` module to extend it and add more functions
for validating more types
See the help for that module for information on other validators.

Added validators:
    cidr
"""

# this module is decorator heaven

import validators
from functools import wraps

def makevalidator(name):
    """decorator for adding validators to this wrapper module"""
    def wrap(f):
        @validators.utils.validator
        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        setattr(validators, name, wrapped)
        return wrapped
    return wrap

@makevalidator('cidr')
def validatecidr(cidr):
    """checks if a string is a valid cidr network"""
    ip, _, mask = cidr.partition('/')
    return validators.ipv4(ip) and int(mask) in range(33)

@makevalidator('number')
def validatenumber(num):
    """checks if a string is a valid decimal number"""
    res = False
    try:
        num = float(num)
        res = isinstance(num, float)
    except ValueError as e:
        pass
    return res

from validators import *

