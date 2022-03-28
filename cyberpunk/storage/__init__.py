"""Module containing various supported audio stores"""

import logging
from typing import Dict, Optional, Protocol, Tuple, Type
from uuid import UUID

from pydub import AudioSegment

from cyberpunk.config import get_config
from cyberpunk.storage.audius import AudiusStorage
from cyberpunk.storage.gcs import GCSStorage
from cyberpunk.storage.http import HttpLoader
from cyberpunk.storage.local import LocalStorage
from cyberpunk.storage.s3 import S3Storage


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
    def __init__(
        self,
        audio_path: str,
        local_storage_base_dir: Optional[str] = None,
        local_results_base_dir: Optional[str] = None,
        s3_loader_bucket: Optional[str] = None,
        s3_loader_base_dir: Optional[str] = None,
        s3_storage_bucket: Optional[str] = None,
        s3_storage_base_dir: Optional[str] = None,
        s3_results_bucket: Optional[str] = None,
        s3_results_base_dir: Optional[str] = None,
    ):
        """Declare variables like base dir"""

        self.http_loader: HttpLoader = HttpLoader()
        self.storage_table: Dict[str, Type[AudioStorageProtocol]] = {
            "local": LocalStorage,
            "s3": S3Storage,
            "gcs": GCSStorage,
            "audius": AudiusStorage,
        }

        # local:s3:audius => [LocalStorage(), S3Storage(), AudiusStorage()]
        self.audio_path = list(
            map(
                lambda x: self.storage_table[x](),
                audio_path.split(":"),
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
        if (
            config.gcs_results_bucket is None
            and config.s3_storage_bucket is None
        ):
            # TODO : save locally
            pass
        elif config.gcs_results_bucket is not None:
            # TODO : save on gcs
            pass
        elif config.s3_storage_bucket is not None:
            # TODO :  save on s3
            pass
        else:
            logging.error("que?")

        processed_filename = f"{request_id}.{file_type}"
        segment.export(
            f"/tmp/{processed_filename}",
            format=file_type,
        )

        return processed_filename


# Audio Storage Singleton
_AUDIO_STORAGE: Optional[AudioStorage] = None


def configure_storage():
    global _AUDIO_STORAGE

    config = get_config()
    assert config is not None

    logging.info(f"configuring audio store")

    _AUDIO_STORAGE = AudioStorage(
        audio_path=config.audio_path,
        local_storage_base_dir=config.local_storage_base_dir,
        local_results_base_dir=config.local_results_base_dir,
        s3_loader_bucket=config.s3_loader_bucket,
        s3_loader_base_dir=config.s3_loader_base_dir,
        s3_storage_bucket=config.s3_storage_bucket,
        s3_storage_base_dir=config.s3_storage_base_dir,
        s3_results_bucket=config.s3_results_bucket,
        s3_results_base_dir=config.s3_results_base_dir,
    )


def get_storage() -> AudioStorage:
    global _AUDIO_STORAGE

    if _AUDIO_STORAGE is None:
        configure_storage()

    assert _AUDIO_STORAGE is not None
    return _AUDIO_STORAGE
