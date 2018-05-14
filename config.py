import sys
import os
import pickle

if sys.platform == "darwin":
    # OS X
    config_file = os.environ['HOME'] + '/Library/Preferences/vc-adp-sync.pickle'
    if not os.path.isfile(config_file):
        default = {
            "vcuser": str(" "),
            "vcpass": str(" "),
            "vcurl": str(" ")
        }
        pickle.dump(default, open(config_file, "wb"))

elif sys.platform == "win32":
    # Windows
    config_path = os.environ['LOCALAPPDATA'] + "/vc-adp-sync"
    config_file = 'vc-adp-sync.pickle'

    if not os.path.isdir(config_path):
        os.makedirs(config_path)

    if not os.path.isfile(config_path + "/" + config_file):
        default = {
            "vcuser": str(" "),
            "vcpass": str(" "),
            "vcurl": str(" ")
        }
        pickle.dump(default, open(config_file, "wb"))


def save_settings(settings):
    """
    Saves settings to the pickle file
    :param settings: dictionary of settings. vcuser, vcpass, vcurl
    :return: nothing
    """
    pickle.dump(settings, open(config_file, "wb"))


def load_settings():
    """
    Get settings from pickle file
    :return: dictionary of settigns
    """
    s = pickle.load(open(config_file, "rb"))
    return s
