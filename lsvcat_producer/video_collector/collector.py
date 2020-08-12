# Standard library imports
import os
import configparser
import sys

# Local application imports
from .sources.collector_factory import CollectorFactory

# Extract configuration file dir abs path
root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    
# Read configuration
config = configparser.ConfigParser()
config.read(os.path.join(root, 'config.ini'))

def get_frame():
    # Load collector specified in the configuration and extract frame
    try:
        specified_collector = config['VIDEO_COLLECTOR']['stream_source']
        collector = CollectorFactory.get_collector(specified_collector)
        stream_url = config['VIDEO_COLLECTOR']['stream_url']
        frame = collector.snap_frame(stream_url)
        return frame
    except Exception as e:
        #TODO log error
        print("Unexpected error:", sys.exc_info()[0])
        raise



