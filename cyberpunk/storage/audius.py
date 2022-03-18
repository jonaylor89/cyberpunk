import logging
import random
from typing import Tuple

import requests
from pydub import AudioSegment


class AudiusStorage:
    def __init__(self):
        self.host = random.choice(
            (requests.get("https://api.audius.co")).json()["data"],
        )

    def __contains__(self, element):
        return self.contains(element)

    def contains(self, key: str) -> bool:
        return True

    def get_segment(self, key: str) -> Tuple[AudioSegment, str]:
        logging.info(f"pulling key from audius: {key}")
        req = requests.get(
            f"{self.host}/v1/tracks/{key}/stream",
            params={"app_name": "cyberpunk"},
        )

        # TODO: there must be a more robust way of saving temporary files like this
        with open(f"/tmp/{key}.mp3", "wb") as tmp_file:
            tmp_file.write(req.content)

        segment = AudioSegment.from_file(f"/tmp/{key}.mp3")

        return segment, f"{key}.mp3"
