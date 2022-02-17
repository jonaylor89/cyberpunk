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

    def save_segment(self, base_filename: str, segment: AudioSegment) -> str:
        """save an audio segment to storage and return the link to it"""


# Audio Storage Singleton
_audio_storage: Optional[AudioStorage] = None


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


def get_storage():
    global _audio_storage

    if _audio_storage is None:
        _audio_storage = configure_storage()

    return _audio_storage
