import random
import requests

from pydub import AudioSegment


class AudiusStorage(object):
    def __init__(self):
        self.host = random.choice(
            (requests.get("https://api.audius.co")).json()["data"]
        )

    def get_segment(self, key: str) -> AudioSegment:
        req = requests.get(
            f"{self.host}/v1/tracks/{key}/stream",
            params={"app_name": "cyberpunk"},
        )

        print(req.json())

        return AudioSegment.empty()

    def save_segment(
        self,
        base_filename: str,
        segment: AudioSegment,
    ) -> str:
        # TODO: export with Filename unique to the stages run (for caching)
        # TODO: All for exporting different file type (e.g. mp3, wav, etc.)
        processed_filename = f"processed_{base_filename}"
        segment.export(f"tmp/{processed_filename}", format="mp3")

        return processed_filename
