import logging
from typing import Dict, Tuple

import requests

from pydub import AudioSegment

from cyberpunk.config import get_config


class LocalStorage:
    def __init__(self):
        config = get_config()
        
        self.base_dir = config.local_storage.storage_base_dir

    def get_segment(self, key: str) -> Tuple[AudioSegment, str]:

        print(key)
        audio_segment: AudioSegment = AudioSegment.empty()

        if key.startswith("https://"):
            logging.info(f"downloading audio file: {key}")
            req = requests.get(key)

            ext = key.split(".")[-1]

            # TODO: there must be a more robust way of saving temperary files like this
            location: str = f"remote-audio.{ext}"
            with open(f"{self.base_dir}{location}", "wb") as tmp_file:
                tmp_file.write(req.content)

            audio_segment = AudioSegment.from_file(
                f"{self.base_dir}{location}",
            )
        else:
            logging.info(f"pulling key from local storage: {key}")

            location = f"{key}"
            audio_segment = AudioSegment.from_file(
                f"{self.base_dir}{location}",
            )

        return audio_segment, location

    def save_segment(
        self,
        base_filename: str,
        segment: AudioSegment,
        file_format: str,
    ) -> str:
        # TODO: export with Filename unique to the stages run (for caching)
        processed_filename = f"processed_{base_filename}.{file_format}"
        segment.export(
            f"{self.base_dir}{processed_filename}",
            format=file_format,
        )

        return processed_filename

    def get_stats(self) -> Dict:
        return {}
