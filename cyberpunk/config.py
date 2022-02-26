"""
Cyberpunk Configuration Module

"""

from typing import Optional

import yaml


class CyberpunkConfig:
    """Global configuration object for Cyberpunk"""

    def __init__(
        self,
        audio_path: str = "local:http",
        local_storage_base_dir: str = "testdata/",
        local_results_base_dir: str = "testdata/",
        s3_loader_bucket: str = "mybucket",
        s3_loader_base_dir: str = "audio/",
        s3_storage_bucket: str = "mybucket",
        s3_storage_base_dir: str = "audio/",
        s3_results_bucket: str = "mybucket",
        s3_results_base_dir: str = "audio/results/",
    ):
        # local | s3 | audius
        self.audio_path = audio_path

        self.local_storage_base_dir = local_storage_base_dir
        self.local_results_base_dir = local_results_base_dir

        self.s3_loader_bucket = s3_loader_bucket
        self.s3_loader_base_dir = s3_loader_base_dir

        self.s3_storage_bucket = s3_storage_bucket
        self.s3_storage_base_dir = s3_storage_base_dir

        self.s3_results_bucket = s3_results_bucket
        self.s3_results_base_dir = s3_results_base_dir

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
    audio_source = data["audio_path"]
    storage_base_dir = data["local_storage_base_dir"]
    s3_storage_bucket = data["s3_storage_bucket"]
    s3_storage_base_dir = data["s3_storage_base_dir"]

    _CYBERPUNK_CONFIG = CyberpunkConfig(
        audio_source,
        storage_base_dir,
        s3_storage_bucket,
        s3_storage_base_dir,
    )


def get_config() -> CyberpunkConfig:
    global _CYBERPUNK_CONFIG

    if _CYBERPUNK_CONFIG is None:
        configure_config()

    assert _CYBERPUNK_CONFIG is not None
    return _CYBERPUNK_CONFIG
