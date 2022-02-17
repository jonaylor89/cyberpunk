from typing import Optional

import yaml


class CyberpunkConfig:
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


class LocalStorageConfig:
    def __init__(self, storage_base_dir: str = "testdata/"):
        self.storage_base_dir = storage_base_dir


class S3StorageConfig:
    def __init__(
        self,
        s3_storage_bucket: str = "mybucket",
        s3_storage_base_dir: str = "audio/",
    ):
        self.s3_storage_bucket = s3_storage_bucket
        self.s3_storage_base_dir = s3_storage_base_dir


_cyberpunk_config: Optional[CyberpunkConfig] = None


def configure_config(path: str = "cyberpunk.yaml"):
    global _cyberpunk_config

    with open(path) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    # TODO: validation lol
    audio_source = data["audio_store"]
    storage_base_dir = data["local"]["storage_base_dir"]
    s3_storage_bucket = data["s3"]["s3_storage_bucket"]
    s3_storage_base_dir = data["s3"]["s3_storage_base_dir"]

    _cyberpunk_config = CyberpunkConfig(
        audio_source,
        storage_base_dir,
        s3_storage_bucket,
        s3_storage_base_dir,
    )


def get_config():
    global _cyberpunk_config

    if _cyberpunk_config is None:
        _cyberpunk_config = configure_storage()

    return _cyberpunk_config
