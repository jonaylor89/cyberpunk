"""
Cyberpunk Configuration Module

"""

from typing import Optional

import yaml


class CyberpunkConfig:
    """Global configuration object for Cyberpunk"""

    def __init__(
        self,
        audio_store: str = "local",
        storage_base_dir: str = "testdata/",
        s3_storage_bucket: str = "mybucket",
        s3_storage_base_dir: str = "audio/",
    ):
        # local | s3 | audius
        self.audio_store = audio_store

        self.local_storage = LocalStorageConfig(storage_base_dir)
        self.s3_storage = S3StorageConfig(
            s3_storage_bucket,
            s3_storage_base_dir,
        )

    def __str__(self):
        return ""

    def __repr__(self):
        return ""


class LocalStorageConfig:
    def __init__(self, storage_base_dir: str = "testdata/"):
        self.storage_base_dir = storage_base_dir

    def __str__(self):
        return ""

    def __repr__(self):
        return ""


class S3StorageConfig:
    def __init__(
        self,
        s3_storage_bucket: str = "mybucket",
        s3_storage_base_dir: str = "audio/",
    ):
        self.s3_storage_bucket = s3_storage_bucket
        self.s3_storage_base_dir = s3_storage_base_dir

    def __str__(self):
        return ""

    def __repr__(self):
        return ""


_CYBERPUNK_CONFIG: Optional[CyberpunkConfig] = None


def configure_config(path: str = "cyberpunk.yaml"):
    global _CYBERPUNK_CONFIG

    with open(path) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    # TODO: validation lol
    audio_source = data["audio_store"]
    storage_base_dir = data["local"]["storage_base_dir"]
    s3_storage_bucket = data["s3"]["s3_storage_bucket"]
    s3_storage_base_dir = data["s3"]["s3_storage_base_dir"]

    _CYBERPUNK_CONFIG = CyberpunkConfig(
        audio_source,
        storage_base_dir,
        s3_storage_bucket,
        s3_storage_base_dir,
    )


def get_config() -> Optional[CyberpunkConfig]:
    global _CYBERPUNK_CONFIG

    if _CYBERPUNK_CONFIG is None:
        configure_config()

    return _CYBERPUNK_CONFIG
