import requests
import math
import time

class Veracross():
    def __init__(self):
        self.rate_limit_remaining = 300
        self.rate_limit_reset = 0

    def pull(self, c, source):
        """
        Get Veracross Data with pagination
        :param c: config dictionary
        :param source: VC Source (households, facstaff, facstaff/99)
        :return: records in a list of dictionaries
        """
        try:
            s = "/" + source + ".json"
            r = requests.get(c["vcurl"] + s,
                             auth=(c["vcuser"],
                                   c["vcpass"]))
            if r.status_code == 200:
                if self.rate_limit_remaining <= 2:
                    print("waiting for rate limit")
                    time.sleep(self.rate_limit_reset + 1)

                if 'X-Total-Count' in r.headers:
                    pages = math.ceil(int(r.headers['X-Total-Count']) / 100)
                else:
                    self.rate_limit_remaining = r.headers['X-Rate-Limit-Remaining']
                    self.rate_limit_reset = r.headers['X-Rate-Limit-Reset']
                    return r.json()

                page = 1
                records = []

                while page <= pages:
                    r = requests.get(c["vcurl"] + s + "?page=" + str(page),
                                     auth=(c["vcuser"],
                                           c["vcpass"]))
                    self.rate_limit_remaining = r.headers['X-Rate-Limit-Remaining']
                    self.rate_limit_reset = r.headers['X-Rate-Limit-Reset']
                    records += r.json()
                    page += 1
                return records
            else:
                return None
        except:
            return None
