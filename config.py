
from configparser import ConfigParser

class NamespacedConfig(ConfigParser, dict):
    pass

class FormitConfig(dict):
    def __init__(self, appname, appslug):
        self['server_root'] = __main__.__file__
        self['index_path'] = ''
        self['script_path'] = ''
        self['ajax_path'] = ''
