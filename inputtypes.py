
import validatorsplus as validators

class InputType:
    def __init__(self, name, format_=None, validator=lambda t: True):
        pass
    def isvalid(self, s):
        return self.validator(s)


strinput = InputType('str')
numinput = InputType('num', validator=validators.number)

