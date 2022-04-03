import logging
import random
from functools import lru_cache
from typing import Optional, Tuple

import requests
from pydub import AudioSegment

MAX_CACHE_SIZE = 50


class AudiusStorage:
    def __init__(self):
        self.host = random.choice(
            (requests.get("https://api.audius.co")).json()["data"],
        )

    def __contains__(self, element):
        return self.contains(element)

    def contains(self, key: str) -> bool:
        print(self.host, key)
        return True

    @lru_cache(MAX_CACHE_SIZE)
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


# Audius Storage Singleton
_AUDIUS_STORAGE: Optional[AudiusStorage] = None


def configure_audius_storage():
    global _AUDIUS_STORAGE

    logging.info(f"configuring audius store")

    _AUDIUS_STORAGE = AudiusStorage()


def get_audius_storage() -> AudiusStorage:
    global _AUDIUS_STORAGE

    if _AUDIUS_STORAGE is None:
        configure_audius_storage()

    assert _AUDIUS_STORAGE is not None
    return _AUDIUS_STORAGE
