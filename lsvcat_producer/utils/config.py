import os
import configparser

# Extract configuration file dir abs path
root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    

# Read configuration
_config = configparser.ConfigParser()
_config.read(os.path.join(root, 'config.ini'))


def config(section, key):
    return _config[section][key]


