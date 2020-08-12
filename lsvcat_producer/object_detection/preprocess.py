# Third party imports
import numpy as np
import cv2

def resize_to_scale(image, width=None, height=None, interpolation=cv2.INTER_AREA):
    final_dimensions = None
    (h,w) = image.shape[:2]

    if width is None and height is None:
        return image
    
    # If width is None scale image size against height
    if width is None:
        # Calculate ratio based on height and new dimensions
        ratio = height / float(h)
        final_dimensions = (int(w * ratio), height)
    else:
        # Calculate ratio based on width and new dimensions
        ratio = width / float(w)
        final_dimensions = (width, int(h * ratio))
    
    resized = cv2.resize(image, final_dimensions, interpolation=interpolation)
    return resized


def expand_image(image_array):
    return np.expand_dims(image_array, axis=0)


def preprocess_image(image_array, target_width=None, target_height=None):
    (h,w) = image_array.shape[:2]

    # Converts an image from BGR to RGB format
    image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    
    # Check desired image size
    input_image = image_array
    if target_width and w != target_width:
        input_image = resize_to_scale(input_image, width=target_width)
    elif target_height and h != target_height:
        input_image = resize_to_scale(input_image, height=target_height)

    preprocessed_img = expand_image(input_image)
    tf_api_parameter = {"instances": preprocessed_img.tolist()}
    return image_array, preprocessed_img, tf_api_parameter