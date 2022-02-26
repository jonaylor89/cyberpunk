import logging
from typing import Dict, Tuple

from pydub import AudioSegment

from cyberpunk.config import get_config


class LocalStorage:
    def __init__(self):
        config = get_config()

        self.base_dir = config.local_storage.storage_base_dir

    def __contains__(self, element):
        return contains(element)

    def contains(self, key: str) -> bool:
        return False

    def get_segment(self, key: str) -> Tuple[AudioSegment, str]:
        logging.info(f"pulling key from local storage: {key}")

        location = f"{key}"
        audio_segment = AudioSegment.from_file(
            f"{self.base_dir}{location}",
        )

        return audio_segment, location

    def get_stats(self) -> Dict:
        return {}
