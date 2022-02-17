import logging
import random

import requests
from pydub import AudioSegment


class AudiusStorage:
    def __init__(self):
        self.host = random.choice(
            (requests.get("https://api.audius.co")).json()["data"],
        )

    def get_segment(self, key: str) -> AudioSegment:
        logging.info(f"pulling key from audius: {key}")
        req = requests.get(
            f"{self.host}/v1/tracks/{key}/stream",
            params={"app_name": "cyberpunk"},
        )

        with open(f"testdata/{key}.mp3", "wb") as tmp_file:
            tmp_file.write(req.content)

        segment = AudioSegment.from_file(f"testdata/{key}.mp3")

        return segment

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
