
import validatorsplus as validators
from datetime import datetime

from compose import FormParam

'''
class FormParam:
    def __init__(self, name, format_=None, validator=lambda t: True):
        pass
    def isvalid(self, s):
        return self.validator(s)
    def tohtml(self):
        pass
'''

class STR(FormParam):
    def __init__(self):
        super().__init__('str')

class ENUM(FormParam):
    def __init__(self, format_=tuple()):
        #use make validator?
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

class TABLE(FormParam):
    def __init__(self, format_):
        # by default, table has no valid inputs, since it's meant for output
        super().__init__('table', format_, lambda t: False)

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

