import logging
from functools import lru_cache
from typing import Tuple

import requests
from pydub import AudioSegment

MAX_CACHE_SIZE = 50


class HttpLoader:
    def __init__(self):
        """Declare variables like base dir"""

    @lru_cache(MAX_CACHE_SIZE)
    def get_segment(self, key: str) -> Tuple[AudioSegment, str]:
        """get an audio segment from storage"""
        logging.info(f"downloading audio file: {key}")
        req = requests.get(key)

        ext = key.split(".")[-1]

        # TODO: there must be a more robust way of saving temporary files like this
        location: str = f"remote-audio.{ext}"
        with open(f"/tmp/{location}", "wb") as tmp_file:
            tmp_file.write(req.content)

        audio_segment = AudioSegment.from_file(
            f"/tmp/{location}",
        )

        return audio_segment, location
