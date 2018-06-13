"""
ADP API Class
Built for Veracross ADP Sync, but can be portable.

Create new object with config as fist parameter.  Config should contain a dictionary that contains at a minimum:
{'adpnetuser': 'xxx-xxxx-xxxx-xxxx-xxxx',
'adpnetpass': 'xxx-xxxx-xxxx-xxxx-xxxx',
'adpcertpath': 'path/to/cert.pem',
'adpcertkeypath': 'path/to/auth.key'
}

Example:
    c = {'adpnetuser': 'xxx-xxxx-xxxx-xxxx-xxxx',
        'adpnetpass': 'xxx-xxxx-xxxx-xxxx-xxxx',
        'adpcertpath': 'path/to/cert.pem',
        'adpcertkeypath': 'path/to/auth.key'
        }
    a = api_api.Adp(c)
    a.get_workers()
"""
import requests
import datetime

__author__ = "Forrest Beck"


class Adp(object):

    def __init__(self, config):
        """
        Creates new ADP object.
        :param config: Specify dictionary with config
        """
        self.oauth_url = "https://accounts.adp.com/auth/oauth/v2/token"
        # Initialize token as expired.
        self.token_expire_time = datetime.datetime.now() - datetime.timedelta(days=1)
        self.bearer_token = ""
        self.config = config
        # Create a new session for API calls. This will bearer token.
        self.session = requests.Session()

    def get_token(self):
        if datetime.datetime.now() > self.token_expire_time:
            """
            Use new session. Leave init session for actual API calls.
            This leaves off the Username and Password when making API calls which only needs 
            bearer token.
            """
            s = requests.Session()
            s.auth = (self.config["adpnetuser"], self.config["adpnetpass"])
            try:
                r = s.post(self.oauth_url + '?grant_type=client_credentials',
                           cert=(self.config['adpcertpath'], self.config['adpcertkeypath']))
                json = r.json()
                self.token_expire_time = datetime.datetime.now() + \
                                         datetime.timedelta(seconds=int(json["expires_in"]))
                self.bearer_token = json["access_token"]
                self.session.headers.update({'Authorization': 'Bearer ' + self.bearer_token})

                return self.bearer_token
            except:
                return None
        else:
            return self.bearer_token

    def get_workers(self):
        # Check token is present and not expired.
        self.get_token()

        try:
            w = self.session.get('https://api.adp.com/hr/v2/worker-demographics')
            r = w.json()
            return r["workers"]
        except:
            return None


