"""Module containing various supported audio stores"""

import logging
from typing import Dict, Optional, Protocol, Tuple
from uuid import UUID

from pydub import AudioSegment

from cyberpunk.config import get_config
from cyberpunk.storage.audius import get_audius_storage
from cyberpunk.storage.gcs import get_gcs_storage
from cyberpunk.storage.http import get_http_loader
from cyberpunk.storage.local import get_local_storage
from cyberpunk.storage.s3 import get_s3_storage


class AudioStorageProtocol(Protocol):
    def __init__(self):
        """Declare variables like base dir"""

    def __contains__(self, element):
        """same as contains"""

    def contains(self, key: str) -> bool:
        """checks if a given key is in the audio store"""

    def get_segment(self, key: str) -> Tuple[AudioSegment, str]:
        """get an audio segment from storage"""


class AudioStorage:
    def __init__(self):
        """Declare variables like base dir"""

        config = get_config()

        self.http_loader = get_http_loader()
        self.storage_table: Dict[str, AudioStorageProtocol] = {
            "local": get_local_storage(),
            "s3": get_s3_storage(),
            "gcs": get_gcs_storage(),
            "audius": get_audius_storage(),
        }

        # local:s3:audius => [LocalStorage(), S3Storage(), AudiusStorage()]
        self.audio_path = list(
            map(
                lambda x: self.storage_table[x],
                config.audio_path.split(":"),
            ),
        )

    def __str__(self):
        return ""

    def __repr__(self):
        return ""

    def __contains__(self, element):
        return self.contains(element)

    def contains(self, key: str) -> bool:
        """checks if a given key is in the audio store"""

        for storage in self.audio_path:
            if key in storage:
                return True

        return False

    def get_segment(self, key: str) -> Tuple[AudioSegment, str]:
        """get an audio segment from storage"""

        if key.startswith("https://") or key.startswith("http://"):
            return self.http_loader.get_segment(key)

        for storage in self.audio_path:
            if storage.contains(key):
                return storage.get_segment(key)

        raise KeyError(
            f"key `{key}` not found in any configured audio store ({self.audio_path})",
        )

    def save_segment(
        self,
        request_id: UUID,
        segment: AudioSegment,
        file_type: str,
    ) -> str:
        """save an audio segment to storage and return the link to it
        @param request_id: the id for the request and the tmp filename
        @param segment: the audio data to be saved
        @param file_type: the audio type to encode the segment
        @return: the tmp location where the processed audio is located
        """

        config = get_config()
        processed_filename = f"{request_id}.{file_type}"

        if config.output_location == "local":
            get_local_storage().save_segment(
                segment,
                processed_filename,
                file_type,
            )
        elif config.output_location == "gcs":
            get_gcs_storage().save_segment(
                segment,
                processed_filename,
                file_type,
            )
        elif config.output_location == "s3":
            get_s3_storage().save_segment(
                segment,
                processed_filename,
                file_type,
            )
        else:
            logging.error("que")

        return processed_filename


# Audio Storage Singleton
_AUDIO_STORAGE: Optional[AudioStorage] = None


def configure_storage():
    global _AUDIO_STORAGE

    logging.info(f"configuring audio store")

    _AUDIO_STORAGE = AudioStorage()


def get_storage() -> AudioStorage:
    global _AUDIO_STORAGE

    if _AUDIO_STORAGE is None:
        configure_storage()

    assert _AUDIO_STORAGE is not None
    return _AUDIO_STORAGE
