"""
ADP API Class
"""
import requests
import datetime

__author__ = "Forrest Beck"


class Adp(object):

    def __init__(self):
        self.oauth_url = "https://accounts.adp.com/auth/oauth/v2/token"
        # Initialize token as expired.
        self.token_expire_time = datetime.datetime.now() - datetime.timedelta(days=1)
        self.bearer_token = ""
        self.session = requests.Session()

    def get_token(self, c):
        if datetime.datetime.now() > self.token_expire_time:
            s = self.session
            s.auth = (c["adpnetuser"], c["adpnetpass"])
            try:
                r = s.post(self.oauth_url + '?grant_type=client_credentials',
                           cert=(c['adpcertpath'], c['adpcertkeypath']))
                json = r.json()
                self.token_expire_time = datetime.datetime.now() + \
                                         datetime.timedelta(seconds=int(json["expires_in"]))
                self.bearer_token = json["access_token"]
                return self.bearer_token
            except:
                return None
        else:
            return self.bearer_token

