# Standard library imports
import os
import configparser

# Third party imports
import requests

# Local application imports
from . import preprocess as prep
from . import postprocess as postp


# Extract configuration file dir abs path
root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    

# Read configuration
config = configparser.ConfigParser()
config.read(os.path.join(root, 'config.ini'))


def process_image(image):
    target_objects = config['DETECTION']['target_objects'].split(',')
    model_input_desired_w = config.getint('DETECTION','input_image_width')
    mask_rcnn_url = config['DETECTION']['serving_url_mask_rcnn']

    original_image, preprocessed_image, api_parameter = prep.preprocess_image(image, target_width=model_input_desired_w)
    
    mask_out = extract_objects(api_parameter, mask_rcnn_url)

    out_statistics = postp.count_detections_of_interest(mask_out, target_objects)

    postp.draw_boxes_and_labels_on_image(original_image, mask_out)

    return out_statistics


def extract_objects(input, url):
    try:
        res = requests.post(url, json=input)
    except requests.exceptions.RequestException:
        #TODO log error
        print("ERROR: Request error, did you start Tensorflow Serving?")
    except Exception as e:
        #TODO log error
        print(e)

    output = res.json()["predictions"][0]
    return output



