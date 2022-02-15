from pydub import AudioSegment
from typing import Protocol, Dict, Type

from storage.local import LocalStorage
from storage.s3 import S3Storage
from storage.audius import AudiusStorage

from config import cyberpunk_config


# Audio Storage Singleton
audio_storage: AudioStorage = configure_storage()


def configure_storage() -> AudioStorage:

    storage_table: Dict[str, Type[AudioStorage]] = {
        "local": LocalStorage,
        "s3": S3Storage,
        "audius": AudiusStorage,
    }
    store = cyberpunk_config.audio_store

    return storage_table[store]()


class AudioStorage(Protocol):
    def __init__(self):
        """Declare variables like base dir"""

    def get_segment(self, key: str) -> AudioSegment:
        """get an audio segment from storage"""

    def save_segment(self, base_filename: str, segment: AudioSegment) -> str:
        """save an audio segment to storage and return the link to it"""
