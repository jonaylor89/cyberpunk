import logging
import random
from typing import Dict

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

        # TODO: there must be a more robust way of saving temperary files like this
        with open(f"testdata/{key}.mp3", "wb") as tmp_file:
            tmp_file.write(req.content)

        segment = AudioSegment.from_file(f"testdata/{key}.mp3")

        return segment

    def save_segment(
        self,
        base_filename: str,
        segment: AudioSegment,
        file_format: str,
    ) -> str:
        # TODO: export with Filename unique to the stages run (for caching)
        processed_filename = f"processed_{base_filename}.{file_format}"
        segment.export(f"tmp/{processed_filename}", format=file_format)

        return processed_filename

    def get_stats(self) -> Dict:
        return {}
