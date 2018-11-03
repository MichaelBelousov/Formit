# Formit

Early tools for generating fullstack PHP web apps from within Python.

This was originally being developed to ease moving a PHP/Python XMLRPC backend stack to pure
Python by generating some PHP boilerplate. Inevitably of course, I moved on (one might ask,
what higher calling is there besides dismantling the heatheness PHP?).

## Usage

```Python

@make_app('My App', 
        approot='/var/www/html/applications', 
        templatepath='/var/www/html/templates')
class YourClass:
    # in retrospect, how did I not think about using function annotations and decorators?
    # why on earth would I use docstrings in a dynamic language with decorators?
    @param(ip=ipv4)
    @result(table('mac', 'building', 'department'))
    def get_data_by_ip(self, ip):
        """
        get data about an IP on our network
        """
        return database.safequery(query, limit=20)

```
