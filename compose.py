
# TODO: use jinja2

from textwrap import dedent
from grammar import pstatement, commands
import jinja2
from datetime import datetime

defaultalert = {
        'hidden' : False,
        'err_on_syntax' : True,
        'never_warn' : False,
        'always_error' : False
        }

class FormApp(dict):
    """
    HTML form-based app assembled from an annotated class
    """

    def __init__(self, cls, name, baseurl, root, template):
        """
        cls: the annotated class
        path: the application target directory
        template: the path to the template directory
        """
        self.root = root
        self.template = template
        self.indexfilename = 'index.php'
        self.params = {}
        self.results = {}
        self['appname'] = name
        self['phplib'] = self.path
        self['jssettings'] = {'base_url': baseurl}

        funcs = [f for f in dir(cls)
                if callable(getattr(cls, f))]

        for func in funcs:
            data = pstatement.parseString(ln)
            if data:
                cmd = data[0]
                args = data[1:]
                commands[cmd](self, args)
        super().__init__()

    def _get_uniq_id(self, prefix='id'):
        filt = (i for i in self.params + self.results
                if i.name.startswith(prefix))
        m = max(filt, key=lambda t: int(t.partition(prefix)[2]))
        return '{prefix}{num}'.format(prefix=prefix, num=m+1)

    def __getitem__(self, key):
        if key == 'params':
            return [i.render() for i in self.params]
        elif key == 'results':
            return [i.render() for i in self.results]
        else:
            return super().__getitem__(key)

    def render(self):
        """renders the form"""
        # render index page
        dest = os.path.join(self.root, self.indexfilename)
        context = self
        context['gentime'] = datetime.now()

        templatepath, templatefname = os.path.split(self.template)
        res = jinja2.Environment(
                loader=jinja2.FileSystemLoader(templatepath)
                ).get_template(templatefname).render(context)
        with open(dest, 'w') as f:
            f.write(res)

        # render script page

class FormElem:

    def __init__(self, parent, label=None, attachpoint='form', 
            template=''):
        self.label = label
        self.attachpoint = 'form'
        self.template = ''
        self.id = None

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

    def getid(self):
        if self.id is None:
            self.id = parent._get_uniq_id()
        return self.id

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

    def __init__(self, type_={}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = type_  # mapping to formats

class TableResult(FormResult):
    """table format result"""
    def __init__(self):
        pass


