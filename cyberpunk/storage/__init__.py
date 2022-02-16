from typing import Dict, Protocol, Type

from pydub import AudioSegment

from cyberpunk.config import cyberpunk_config
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


def configure_storage() -> AudioStorage:

    storage_table: Dict[str, Type[AudioStorage]] = {
        "local": LocalStorage,
        "s3": S3Storage,
        "audius": AudiusStorage,
    }
    store = cyberpunk_config.audio_store

    return storage_table[store]()


# Audio Storage Singleton
audio_storage: AudioStorage = configure_storage()
