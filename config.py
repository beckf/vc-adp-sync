import sys
import os
import shelve

if sys.platform == "darwin":
    # OS X
    config_file = os.environ['HOME'] + '/Library/Preferences/vc-adp-sync'

elif sys.platform == "win32":
    # Windows
    config_file = os.environ['LOCALAPPDATA'] + "/vc-adp-sync"

else:
    config_file = "/vc-adp-sync"

if not os.path.isfile(config_file + ".db"):
    default = {}
    d = shelve.open(config_file, flag='c', writeback=True)
    d["config"] = default
    d["fields"] = default
    d.sync()
    d.close()


def save_settings(settings, key):
    """
    Saves settings to the pickle file
    :param settings:  data to save.
    :param key: shelve key to save the data to
    :return: nothing
    """
    d = shelve.open(config_file, flag='c', writeback=True)
    d[key] = settings
    d.sync()
    d.close()


def load_settings(key):
    """
    Get settings from pickle file
    :return: data from file
    """
    d = shelve.open(config_file, flag='c', writeback=True)
    s = d[key]
    d.close()
    return s
