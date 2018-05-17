import requests
import math
import time

"""
Veracross API Class

This class gives you an easy interface to the Veracross API through your python scripts.

Example of instantiating the class:

import veracross_api as v
vc = Veracross()
vc.session.auth = ("apiusername", "apipassword")
vc.base_url = "https://api.veracroos.com/XX/v2"
data = vc.pull("facstaff")

"""

__author__ = "Forrest Beck"

class Veracross(object):
    def __init__(self):
        self.rate_limit_remaining = 300
        self.rate_limit_reset = 0
        self.session = requests.Session()
        self.base_url = "https://api.veracross.com/XX/v2"

    def set_timers(self, limit_remaining, limit_reset):
        """
        Sets the rate limits
        :param limit_remaining: Count of API calls remaining from header X-Rate-Limit-Remaining
        :param limit_reset: Reset Timer from header X-Rate-Limit-Reset
        :return: nothing
        """
        self.rate_limit_remaining = int(limit_remaining)
        self.rate_limit_reset = int(limit_reset)
        print(self.rate_limit_remaining)
        if self.rate_limit_remaining == 1:
            print("waiting for vc rate limit:" + str(self.rate_limit_reset))
            time.sleep(self.rate_limit_reset + 1)

    def pull(self, source):
        """
        Get Veracross Data with pagination
        :param c: config dictionary (see config.py)
        :param source: VC Source (households, facstaff, facstaff/99)
        :return: records in a list of dictionaries
        """
        try:
            s = self.base_url + "/" + source + ".json"
            r = self.session.get(s)

            if r.status_code == 200:

                if 'X-Total-Count' in r.headers:
                    pages = math.ceil(int(r.headers['X-Total-Count']) / 100)
                else:
                    self.set_timers(r.headers['X-Rate-Limit-Remaining'],
                                    r.headers['X-Rate-Limit-Reset'])
                    return r.json()

                page = 1
                records = []

                while page <= pages:
                    self.set_timers(r.headers['X-Rate-Limit-Remaining'],
                                    r.headers['X-Rate-Limit-Reset'])
                    r = self.session.get(s + "?page=" + str(page))

                    records += r.json()
                    page += 1
                return records
            else:
                return None
        except:
            return None
