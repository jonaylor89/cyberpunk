"""
Cyberpunk Configuration Module

"""
import os
from typing import Optional


class CyberpunkConfigException(Exception):
    pass


class CyberpunkConfig:
    """Global configuration object for Cyberpunk"""

    def __init__(
        self,
        audio_path: str = "local",
        local_storage_base_dir: Optional[str] = "testdata/",
        local_results_base_dir: Optional[str] = None,
        s3_loader_bucket: Optional[str] = None,
        s3_loader_base_dir: Optional[str] = None,
        s3_storage_bucket: Optional[str] = None,
        s3_storage_base_dir: Optional[str] = None,
        s3_results_bucket: Optional[str] = None,
        s3_results_base_dir: Optional[str] = None,
        jaeger_tracing: Optional[bool] = False,
        jaeger_agent_hostname: Optional[str] = "jaeger",
        jaeger_agent_port: Optional[int] = 6831,
        gcp_tracing: Optional[bool] = False,
    ):

        # TODO: validation lol

        # local | s3 | audius
        self.audio_path = audio_path

        if (
            "local" in self.audio_path.split(":")
            and local_storage_base_dir is None
        ):
            raise CyberpunkConfigException(
                "local_storage_base_dir must be configured if `local` in audio_path",
            )

        self.local_storage_base_dir = local_storage_base_dir
        self.local_results_base_dir = local_results_base_dir

        if "s3" in self.audio_path.split(":") and s3_storage_bucket is None:
            raise CyberpunkConfigException(
                "s3_storage_bucket must be configured if `s3` in audio_path",
            )

        self.s3_loader_bucket = s3_loader_bucket
        self.s3_loader_base_dir = s3_loader_base_dir

        self.s3_storage_bucket = s3_storage_bucket
        self.s3_storage_base_dir = s3_storage_base_dir

        self.s3_results_bucket = s3_results_bucket
        self.s3_results_base_dir = s3_results_base_dir

        self.jaeger_tracing = jaeger_tracing
        self.jaeger_agent_hostname = jaeger_agent_hostname
        self.jaeger_agent_port = jaeger_agent_port

        self.gcp_tracing = gcp_tracing

    def __repr__(self):
        return (
            f"CyberpunkConfig ( "
            f"audio_path: {self.audio_path}, "
            f"local_storage_base_dir: {self.local_storage_base_dir}, "
            f"local_results_base_dir: {self.local_results_base_dir} "
            f")"
        )


_CYBERPUNK_CONFIG: Optional[CyberpunkConfig] = None


def configure_config(provided_config: Optional[CyberpunkConfig] = None):
    global _CYBERPUNK_CONFIG

    if provided_config is not None:
        _CYBERPUNK_CONFIG = provided_config
    else:
        _CYBERPUNK_CONFIG = CyberpunkConfig(
            audio_path=os.environ.get("AUDIO_PATH", "local"),
            local_storage_base_dir=os.environ.get(
                "LOCAL_STORAGE_BASE_DIR",
                "testdata/",
            ),
            local_results_base_dir=os.environ.get(
                "LOCAL_RESULTS_BASE_DIR",
                None,
            ),
            s3_loader_bucket=os.environ.get("S3_LOADER_BUCKET", None),
            s3_loader_base_dir=os.environ.get("S3_LOADER_BASE_DIR", None),
            s3_storage_bucket=os.environ.get("S3_STORAGE_BUCKET", None),
            s3_storage_base_dir=os.environ.get("S3_STORAGE_BASE_DIR", None),
            s3_results_bucket=os.environ.get("S3_RESULTS_BUCKET", None),
            s3_results_base_dir=os.environ.get("S3_RESULTS_BASE_DIR", None),
            jaeger_tracing=os.environ.get(
                "JAEGER_TRACING_ENABLED",
                "0",
            ).lower()
            in ("true", "1", "t"),
            jaeger_agent_hostname=os.environ.get(
                "JAEGER_AGENT_HOSTNAME",
                "jaeger",
            ),
            jaeger_agent_port=int(os.environ.get("JAEGER_AGENT_PORT", "6831")),
            gcp_tracing=os.environ.get("GCP_TRACING_ENABLED", "0").lower()
            in ("true", "1", "t"),
        )


def get_config() -> CyberpunkConfig:
    global _CYBERPUNK_CONFIG

    if _CYBERPUNK_CONFIG is None:
        configure_config()

    assert _CYBERPUNK_CONFIG is not None
    return _CYBERPUNK_CONFIG
