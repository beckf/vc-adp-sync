import requests
import math


def fs(c, source):
    """
    Get Veracross Data with pagination
    :param c: config dict
    :param source: VC Source (households, facstaff, facstaff/99)
    :return: records in a list of dictionaries
    """
    try:
        s = "/" + source + ".json"
        r = requests.get(c["vcurl"] + s,
                         auth=(c["vcuser"],
                               c["vcpass"]))
        if r.status_code == 200:
            if 'X-Total-Count' in r.headers:
                pages = math.ceil(int(r.headers['X-Total-Count']) / 100)
            else:
                return r.json()
            page = 1
            records = []
            while page <= pages:
                r = requests.get(c["vcurl"] + s + "?page=" + str(page),
                                 auth=(c["vcuser"],
                                       c["vcpass"]))
                records += r.json()
                page += 1
            return records
        else:
            return None
    except:
        return None
