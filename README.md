# Formit

Early tools for generating HTML forms app frontends from simple python docstring annotations

## Goals

##### Extensibility

This project was originally designed for a PHP/Python XMLRPC stack, 
it should be easily extendable to other web stacks with minimal work, and high
convenience, using simple templates, and a well structured API.

Such extensions should be complete externally, perhaps by using a metaclass 
instead of a decorator, so inheritance can be used.

Users should be able to add their own types, with their own validation, and more.

##### Configurability

Users should be able to, without a painful amount of decorator arguments, 
augment all necessary features for any server configuration, or app intent.

##### Heuristics

Users should be able to externally add hueristic formatting.

For instance, it should be possible to add concepts such as "if there are many buttons in the form, add a *select all* and a *select none* button to them".

##### Robustness

Unit tests should be used to ensure informed exceptions for all configurations and programmer errors.

## Usage

```Python

@make_app('My App', 
        approot='/var/www/html/applications', 
        templatepath='/var/www/html/templates')
class YourClass:
    def get_data_by_ip(self, ip):
        """
        get data about an IP on our network

        !group search  # we don't really need a group for one function
        @param[ipv4] ip
        @result[table|mac, building, department]
        """
        return database.safequery(query, limit=20)

```

That's all it takes, some simple docstring annotation which is already inherent 
in the design of your backend, and a decorator.

The PHP AJAX endpoints, PHP/HTML form, clientside validation code for form input, and etc are all generated using jinja2.

