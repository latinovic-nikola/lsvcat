# Local application import
from video_collector import collector
from object_detection import process


# Load livestream image
image_frame = collector.get_frame()
if image_frame is not None:
    s1 = process.process_image(image_frame)
    print(s1)