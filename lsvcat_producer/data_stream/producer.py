import os
from utils.config import config
from video_collector import collector
from object_detection.process import process_image
from weather.download_weather_info import get_current_weather
from confluent_kafka import Producer
import json


def format_data():
    # Load image
    try:
        image_frame = collector.get_frame()
        if image_frame is not None:

            result = {}
            object_count = process_image(image_frame)
            weather = get_current_weather()
            
            result['timestamp'] = int(weather['dt']) + int(weather['timezone'])
            result['location'] = config('VIDEO_COLLECTOR', 'stream_place')
            for key in object_count:
                result[key + '_no'] = object_count[key]
            result['temp'] = weather['main']['temp']
            result['temp_feels_like'] = weather['main']['feels_like']
            result['temp_min'] = weather['main']['temp_min']
            result['temp_max'] = weather['main']['temp_max']
            result['pressure'] = weather['main']['pressure']
            result['humidity'] = weather['main']['humidity']
            result['visibility'] = weather['visibility']
            result['wind_speed'] = weather['wind']['speed']
            result['wind_deg'] = weather['wind']['deg']

            return result
    except Exception as e:
        #TODO log error
        print(e)
        return None

def produce_data():
    bootstrap_server = config('KAFKA', 'bootstrap_servers')
    broker_topic = config('KAFKA','default_topic')

    p = Producer({'bootstrap.servers': bootstrap_server})

    def delivery_report(err, msg):
        #TODO change out to logs
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered') 

    data = format_data()
    if data is not None:
        print('\nPublishing data\n')
        p.poll(0)
        p.produce(broker_topic, json.dumps(data), callback=delivery_report)

        r=p.flush(timeout=5)
        if r>0:
            print(f'Message delivery failed ({r} message(s) still remain, did we timeout sending perhaps?)\n')


if __name__ == "__main__":
    import time
    try:
        while True:
            t = time.strftime("%H:%M:%S",  time.localtime())
            print(f'Producing data at -> {t}')
            produce_data()
            print('Sleeping for 20 minutes.')
            time.sleep(1200)
    except Exception as e:
        print('Error occured: %s' % str(e))
