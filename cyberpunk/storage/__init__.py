"""Module containing various supported audio stores"""

import logging
from typing import Dict, Optional, Protocol, Type

from pydub import AudioSegment

from cyberpunk.config import get_config
from cyberpunk.storage.audius import AudiusStorage
from cyberpunk.storage.local import LocalStorage
from cyberpunk.storage.s3 import S3Storage


class AudioStorage(Protocol):
    def __init__(self):
        """Declare variables like base dir"""

    def get_segment(self, key: str) -> AudioSegment:
        """get an audio segment from storage"""

    def save_segment(
        self,
        base_filename: str,
        segment: AudioSegment,
        file_format: str,
    ) -> str:
        """save an audio segment to storage and return the link to it"""

    def get_stats(self) -> Dict:
        """get the stats for that specific storage backend"""


# Audio Storage Singleton
_AUDIO_STORAGE: Optional[AudioStorage] = None


def configure_storage() -> AudioStorage:

    config = get_config()
    assert config is not None

    logging.info(f"configuring audio store: {config.audio_store}")

    storage_table: Dict[str, Type[AudioStorage]] = {
        "local": LocalStorage,
        "s3": S3Storage,
        "audius": AudiusStorage,
    }
    store = config.audio_store

    return storage_table[store]()


def get_storage() -> AudioStorage:
    global _AUDIO_STORAGE

    if _AUDIO_STORAGE is None:
        _AUDIO_STORAGE = configure_storage()

    assert _AUDIO_STORAGE is not None
    return _AUDIO_STORAGE
