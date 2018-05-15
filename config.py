import sys
import os
import shelve

if sys.platform == "darwin":
    # OS X
    config_file = os.environ['HOME'] + '/Library/Preferences/vc-adp-sync'
    if not os.path.isfile(config_file + ".db"):
        default = {
            "vcuser": str(" "),
            "vcpass": str(" "),
            "vcurl": str(" ")
        }
        d = shelve.open(config_file, flag='c', writeback=True)
        d["config"] = default
        d.sync()
        d.close()

elif sys.platform == "win32":
    # Windows
    config_path = os.environ['LOCALAPPDATA'] + "/vc-adp-sync"
    config_file = config_path + "/vc-adp-sync"

    if not os.path.isdir(config_path):
        os.makedirs(config_path)

    if not os.path.isfile(config_file + ".db"):
        default = {
            "vcuser": str(" "),
            "vcpass": str(" "),
            "vcurl": str(" ")
        }
        d = shelve.open(config_file, flag='c', writeback=True)
        d["config"] = default
        d.sync()
        d.close()


def save_settings(settings):
    """
    Saves settings to the pickle file
    :param settings: dictionary of settings. vcuser, vcpass, vcurl
    :return: nothing
    """
    d = shelve.open(config_file, flag='c', writeback=True)
    d["config"] = settings
    d.sync()
    d.close()


def load_settings():
    """
    Get settings from pickle file
    :return: dictionary of settigns
    """
    d = shelve.open(config_file, flag='c', writeback=True)
    s = d["config"]
    d.close()
    return s


def save_field_maps(maps):
    """
    Saves field maps to config file
    :param maps:
    :return: nothing
    """
    try:
        d = shelve.open(config_file, flag='c', writeback=True)
        d["fields"] = maps
        d.sync()
        d.close()
    except:
        return None


def load_field_maps():
    """
    Returns field maps from config file
    :return:
    """
    try:
        d = shelve.open(config_file, flag='c', writeback=True)
        s = d["fields"]
        d.close()
        return s
    except:
        return None
