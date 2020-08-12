# Third party imports
import pafy
import youtube_dl
import cv2


class CollectorYouTube:

    def snap_frame(self, url):
        video = pafy.new(url)
        best = video.getbest(preftype="mp4")
        capture = cv2.VideoCapture(best.url)
        is_valid, image_frame = capture.read()
        return image_frame if is_valid else None



    




