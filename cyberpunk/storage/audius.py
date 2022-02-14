import random
import requests

from pydub import AudioSegment


class AudiusStorage(object):
    def __init__(self):
        self.host = random.choice(
            (requests.get("https://api.audius.co")).json()["data"]
        )

    def get_segment(self, key: str) -> AudioSegment:
        r = requests.get(
            f"{self.host}/v1/tracks/{key}/stream",
            params={"app_name": "cyberpunk"},
        )

        print(r.json())

        return AudioSegment.empty()

    def save_segment(self, base_filename: str, segment: AudioSegment):
        pass
