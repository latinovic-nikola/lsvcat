# Standard library imports
import os
import pickle

# Third party imports
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def load_coco_labels():
    labels_pkl = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'labels/coco.pkl')
    with open(labels_pkl, 'rb') as f:
        return pickle.load(f)


def count_detections_of_interest(model_output, valid_labels, threshold=.5):
    labels = load_coco_labels()
    counter = dict([(key, 0) for key in valid_labels])

    for index in range(len(model_output['detection_boxes'])):
        score = model_output['detection_scores'][index]
        
        if score <= threshold:
            continue
        
        class_name = labels[model_output['detection_classes']
                                        [index]]['name']
        
        if class_name not in valid_labels:
            continue

        counter[class_name] += 1
    return counter
    

""""
Visualize

"""

_COLORS_BUCKET = [
    'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
    'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
    'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
    'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
    'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
    'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
    'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
    'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
    'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
    'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
    'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
    'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
    'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
    'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
    'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
    'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
    'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
    'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
    'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
    'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
    'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
    'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
    'WhiteSmoke', 'Yellow', 'YellowGreen'
]


def draw_boxes_and_labels_on_image(image, model_output, score_threshold = .5, line_thickness=2, keep_images=True):
    boxes = model_output['detection_boxes']
    detected_classes = model_output['detection_classes']
    detected_scores = model_output['detection_scores']

    label_2_color_map = {}
    tmp_image = Image.fromarray(np.uint8(image)).convert('RGB')
    _width, _height = tmp_image.size
    _font = ImageFont.load_default()

    labels = load_coco_labels()

    # Filter boxes based on threshold
    valid_box_indicies = [idx for idx, score in enumerate(detected_scores) if score > score_threshold]
    for i in valid_box_indicies:
        box = tuple(boxes[i])

        # Check for label
        detected_label = 'N\A' 
        if detected_classes[i] in labels.keys():
            detected_label = labels[detected_classes[i]]['name']

        object_title = f'{detected_label}: {int(100*detected_scores[i])}'

        # Select color of bounding box for label
        if detected_label not in label_2_color_map.keys():
            label_2_color_map[detected_label] = _COLORS_BUCKET[len(label_2_color_map.keys())]
        
        draw = ImageDraw.Draw(tmp_image)
        
        # Normalize coordinates of the boxes acording to the original image size
        (left, right, top, bottom) = (box[1] * _width, box[3] * _width, box[0] * _height, box[2] * _height)
        draw.line([(left,top),(left,bottom),(right, bottom), (right, top), (left,top)], 
                    width=line_thickness, fill=label_2_color_map[detected_label])
        
        # Check total height of the image in regards to bbox and labels that should be displayed
        text_height = _font.getsize(object_title)[1]

        # Each text has a top and bottom margin of 0.05x.
        text_display_height = (1 + 2 * 0.05) * text_height

        if top > text_display_height:
            text_bottom_line = top
        else:
            text_bottom_line = bottom + text_display_height

        text_width, text_height = _font.getsize(object_title)
        margin = np.ceil(0.05*text_height)
        draw.rectangle([(left, text_bottom_line - text_height - 2 * margin), (left + text_width, text_bottom_line)], 
                    fill=label_2_color_map[detected_label])
        draw.text((left + margin, text_bottom_line - text_height - margin), object_title, fill='black', font=_font)

    if keep_images:
        from datetime import datetime
        now = datetime.now().strftime("%d-%m-%y-%H-%M")

        relative_path_root = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'images')

        # Save original image
        oimg = Image.fromarray(np.uint8(image)).convert('RGB')
        oimg.save(os.path.join(relative_path_root, 'input', f'{now}_input.png'))
        # Save processed image
        tmp_image.save(os.path.join(relative_path_root, 'output', f'{now}_output.png'))
        
    return tmp_image



            


        
