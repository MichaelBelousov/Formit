
"""
An example class, for guiding development, testing,
and demonstration.
"""

from formit import make_app
from formit.config import FormConfig, FormParam, FormResult

# custom result class
class Chart(FormResult):
    """generate a result chart"""
    name = 'chart'
    def __init__(self):
        super().__init__()

# custom config for adding custom input type
class AppConf(FormConfig):
    """
    custom app config to tweak some directory structure and
    recognize our custom result type
    """
    def __init__(self):
        super().__init__()
        self.appsroot = '/var/www/html/somewhere/MyApp/',
        baseurl = 'https://example.com',
        outtypes.append(CustomChart)


# actual app with a form, the rest of the stuff can all 
# be placed elsewhere and imported  to remove bloat
@make_app('My App', config=AppConf())
class MyApp:
    def __init__(self):
        self.db = None 

    def lookup_user(self, user):
        """
        Look up a user in the user table
        @param[re|/[a-Z]{3}[0-9]{5}/] user
        @result[table|user, ip, mac]
        """
        # this is reminiscent of some db apis, don't worry about it
        table = self.db.query(
                """select (user, ip, mac) from users"""
                """where user=%s...""", 
                user)
        return table

    def see_inactive_users(self):
        """
        See currently inactive users
        @result[table|user]
        """
        # table result class merely expects an iterator of iterators
        return [('Mike', 'Dan', 'Gabe')]
    
    def chart_user_activity(self):
        """
        return a pie chart of user activity
        @result[chart] result
        """
        chart = self.db.query(
                """select (user, logincount) from users"""
                """sorted descending by logincount""")
        return chart
