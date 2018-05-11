import requests
import math


def fs(apiurl, apiuser, apipass):
    """
    Get Veracross Faculty Staff with pagination
    :param apiurl:
    :param apiuser:
    :param apipass:
    :return: records in a list of dictionaries
    """
    try:
        r = requests.get(apiurl + "/facstaff.json", auth=(apiuser, apipass))
        if r.status_code == 200:
            pages = math.ceil(int(r.headers['X-Total-Count']) / 100)
            page = 1
            records = []
            while page <= pages:
                r = requests.get(apiurl + "/facstaff.json?page=" + str(page), auth=(apiuser, apipass))
                records += r.json()
                page += 1
            return records
        else:
            return None
    except:
        return None


def parse_fs(fsdata):
    """
    Revuild VC data for faculty staff to identify only what we want.
    For now, lets cast all as a string.  We can recast when interfaced with api.
    Use person_pk/employee_number as index to keep array sorted.
    :param fsdata:
    :return:
    """
    d = []
    for i in fsdata:
        a = {
            "employee_number": str(i["person_pk"]),
            "last_name": str(i["last_name"]),
            "first_name": str(i["first_name"])
        }
        d.insert(int(i["person_pk"]), a)
    return d
