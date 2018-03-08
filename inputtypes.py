
"""
Input type definitions for formit
"""

import validatorsplus as validators
from datetime import datetime

from compose import FormParam

class STR(FormParam):
    def __init__(self):
        super().__init__('str')

class ENUM(FormParam):
    def __init__(self, format_=tuple()):
        # use make validator?
        @validators.utils.validator
        def v(s, format_=format_):
            return s in format_
        super().__init__('enum', format_, v)

class NUM(FormParam):
    def __init__(self):
        super().__init__('num', None, validators.number)

class CIDR(FormParam):
    def __init__(self):
        super().__init__('cidr', None, validators.cidr)

class IPV4(FormParam):
    def __init__(self):
        super().__init__('ip', None, validators.ipv4)

class MAC(FormParam):
    def __init__(self):
        super().__init__('mac', None, validators.mac_address)

class DATETIME(FormParam):
    def __init__(self, format_):
        @validators.utils.validator
        def v(s, format_=format_):
            res = False
            try:
                s = datetime.strptime(s, format_)
                res = isinstance(s, datetime)
            except:
                pass
            return res
        super().__init__('datetime', format_, v)

