"""
FormConfig for use by formit apps

The default directory structure generated around
the server, henceforth server.py is as follows:

server_root/
    server.py
    templates/
        apptemplate.php

/var/www/html/apps/
    app_slug1/
        app.php
        app.js
        app.css
        ajax/
            app_slug1_ajax_endpoint1.php
        
"""

from configparser import ConfigParser
from inputtypes import *
# import outputtypes as outtypes

class FormConfig(dict):
    """
    A class that stores configuration values
    for form apps, particularly paths, and 
    allows it to be loaded from ini files
    """
    def __init__(self,
            appsroot = '/var/www/html/apps',
            baseurl = 'https://localhost',
            serverroot, _ = os.path.splitext(__main__.__file__),
            jspath = '.',
            csspath = '.',
            ajaxpath = 'ajax/',
            templatespath = os.path.join(serverroot, 'templates/'),
            phplibpath = None,
            **kwargs):
        """init FormConfig"""
        self.update(kwargs)
        self.intypes = [STR, ENUM, NUM, CIDR, IPV4, MAC, DATETIME]
        self.outtypes = []
        self['appsroot'] = appsroot
        self['serverroot'] = serverroot
        self['jspath'] = jspath
        self['csspath'] = csspath
        self['ajaxpath'] = ajaxpath
        self['templatespath'] = templatespath

    def from_ini(ini, sect):
        """load values from an ini file"""
        parser = ConfigParser()
        parser.read(ini)
        for c in parser[sect]
            self[c] = parser[sect][c]

