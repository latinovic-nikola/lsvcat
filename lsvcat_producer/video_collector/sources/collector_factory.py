# Local application imports
from .youtube import CollectorYouTube

class CollectorFactory:

    @staticmethod
    def get_collector(source):
        if source == "youtube":
            return CollectorYouTube()
        else:
            raise ValueError(source)
