import logging
from functools import lru_cache
from typing import Tuple

from pydub import AudioSegment

from cyberpunk.config import get_config

AUDIO_CACHE_SIZE = 50


class LocalStorage:
    def __init__(self):
        config = get_config()

        self.base_dir = config.local_storage_base_dir

    def __contains__(self, element):
        return self.contains(element)

    def contains(self, key: str) -> bool:
        return True

    @lru_cache(AUDIO_CACHE_SIZE)
    def get_segment(self, key: str) -> Tuple[AudioSegment, str]:
        logging.info(f"pulling key from local storage: {key}")

        location = f"{key}"
        audio_segment = AudioSegment.from_file(
            f"{self.base_dir}{location}",
        )

        return audio_segment, location

    def save_segment(self, segment: AudioSegment, key: str, file_type: str):
        logging.debug(f"exporting segment {key} to tmp dir")
        segment.export(
            f"/tmp/{key}",
            format=file_type,
        )
