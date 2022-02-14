import random
import requests

from pydub import AudioSegment

class AudiusStorage(object):

    def __init__(self):
        self.host = random.choice((requests.get("https://api.audius.co")).json()["data"])

    def get_segment(self, key: str) -> AudioSegment:
        pass

    def save_segment(self, base_filename: str, segment: AudioSegment):
        pass