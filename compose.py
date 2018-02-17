
# TODO: use jinja2

from textwrap import dedent

defaultalert = {
        'hidden' : False,
        'err_on_syntax' : True,
        'never_warn' : False,
        'always_error' : False
        }

class Form:
    """Form data, assembled from the given class"""

    def __init__(self):
        inputs = []
        results = []
        scriptblocks = set()  # XXX: oset?
        # move this to some hueristic prettifier algorithm?
        if sum(map(lambda t: isinstance(t, buttonparam), inputs)) > 3:
            # add an all and a none button?
            pass

    def tohtml(self):
        # templates.render()
        # let's use jinja here?
        # render(templatepath)
        return str()

    def addInput(formelem, group=None):
        pass


class FormElem:

    def __init__(self, label=None, attachpoint='form', 
            template=''):
        self.label = label
        self.attachpoint = 'form'
        self.template = ''

    def tohtml(self, **kwargs):
        """generate the html for this form element"""
        kwargs.update(dir(self))  
        return self.template.format(**kwargs)
        # my text editor shuns the double unpack
        # return self.template.format(**kwargs, **dir(self))

    def __format__(self, *args, **kwargs):
        return self.tohtml().format(*args, **kwargs)

    def __str__(self):
        return self.template  #.format(**dir(self))?

class FormParam(FormElem):
    """base class for all params"""
    def __init__(types={}, alert=defaultalert, settings=tuple()
            *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.types = types  # mapping to formats
        self.alert = alert
        self.settings = settings

class MultiFormParam(FormParam):
    def __init__(self, *args):
        if not any(
                map(lambda t: isinstance(t, FormParam), 
                    args)):
            raise TypeError('MultiFormParam takes only '
                    ' FormParam subclasses as arguments')


class SearchParam(FormParam):
    """searchbox format parameter"""
    def __init__(self, label, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template = dedent("""\
            <div class="col-lg-6">
                <h3>{{ label }}</h3>
                <div class="row">
                    <div class="col-lg-8">
                        <div class="input-group">
                            <input type="text" name="{{id}}" id="{{id}}" class="form-control" type="submit" placeholder="{{placeholdertext}}" data-placement="top" data-trigger="focus" data-content="{{placeholder}}">
                            <span class="input-group-btn">
                                <button class="btn btn-primary">Search</button>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            """)

class ButtonParam(Formparam):
    """button format param"""
    def __init__(self, setting, *args, **kwargs):
        super().__init__(types={'bool':None}, *args, **kwargs)
        self.settings.append(setting)
        self.template = dedent("""\
            <div class="col-md-1">
                <label class="pull-right">
                    <input type="checkbox" aria-label="{{label}}" id="{{label}}" name="{{label}}"> {{label}}
                </label>
            </div>
            """)

class StrButtonParam(Formparam):
    """button format param"""
    def __init__(self, setting, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings.append(setting)
        self.template = dedent("""\
            <div class="col-md-1">
                <label class="pull-right">
                    <input type="checkbox" aria-label="{{label}}" id="{{label}}" name="{{label}}"> {{label}}
                </label>
            </div>
            """)


class FormResult(FormElem):
    """base class for all results"""

    def __init__(type_={}, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.type = type_  # mapping to formats

class TableResult(FormResult):
    """table format result"""
    def __init__(self, 


inputvalidators = {
    'num' :
"""\
function isNum(n) {
    return !isNaN(n);
}
""",

}


