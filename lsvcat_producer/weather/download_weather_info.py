# Standard library imports
import os
import configparser

# Third party imports
import requests
import json


# Extract configuration file dir abs path
root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    
# Read configuration
config = configparser.ConfigParser()
config.read(os.path.join(root, 'config.ini'))
config = config['WEATHER']



def get_current_weather():
    (lat, lon) = config['location_lat_lon'].split(',')
    api_key = config['openweathermap_api_key']
    api_url = config['openweathermap_api_url'].format(lat, lon, api_key)
    
    try:
        res = requests.get(api_url)
        weather = json.loads(res.text)
        return weather
    except Exception as e:
        #TODO log error
        print(e)
        return None



