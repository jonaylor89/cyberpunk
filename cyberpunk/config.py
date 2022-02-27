"""
Cyberpunk Configuration Module

"""

from typing import Optional


class CyberpunkConfig:
    """Global configuration object for Cyberpunk"""

    def __init__(
        self,
        audio_path: str = "local",
        local_storage_base_dir: Optional[str] = "testdata/",
        local_results_base_dir: Optional[str] = "testdata/",
        s3_loader_bucket: Optional[str] = None,
        s3_loader_base_dir: Optional[str] = None,
        s3_storage_bucket: Optional[str] = None,
        s3_storage_base_dir: Optional[str] = None,
        s3_results_bucket: Optional[str] = None,
        s3_results_base_dir: Optional[str] = None,
    ):

        # TODO: validation lol

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


def configure_config(provided_config: Optional[CyberpunkConfig] = None):
    global _CYBERPUNK_CONFIG

    if provided_config is not None:
        _CYBERPUNK_CONFIG = provided_config
    else:
        _CYBERPUNK_CONFIG = CyberpunkConfig()


def get_config() -> CyberpunkConfig:
    global _CYBERPUNK_CONFIG

    if _CYBERPUNK_CONFIG is None:
        configure_config()

    assert _CYBERPUNK_CONFIG is not None
    return _CYBERPUNK_CONFIG
