import sys
import os
import pickle

if sys.platform == "darwin":
    # OS X
    config_file = os.environ['HOME'] + '/Library/Preferences/vcadpsync.p'
    if not os.path.isfile(config_file):
        default = {
            "vcuser": str(" "),
            "vcpass": str(" "),
            "vcurl": str(" ")
        }
        pickle.dump(default, open(config_file, "wb"))

elif sys.platform == "win32":
    # Windows
    config_file = 'someplace'
    if not os.path.isfile(config_file):
        open(config_file, 'w').close()


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
