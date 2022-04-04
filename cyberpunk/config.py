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
        debug: bool = True,
        port: int = 8080,
        audio_path: str = "local",
        output_location: str = "local",
        local_storage_base_dir: Optional[str] = "testdata/",
        # s3_loader_bucket: Optional[str] = None,
        # s3_loader_base_dir: Optional[str] = None,
        s3_storage_bucket: Optional[str] = None,
        s3_storage_base_dir: Optional[str] = None,
        s3_results_bucket: Optional[str] = None,
        s3_results_base_dir: Optional[str] = None,
        google_application_credentials: Optional[str] = None,
        # gcs_loader_bucket: Optional[str] = None,
        # gcs_loader_base_dir: Optional[str] = None,
        gcs_storage_bucket: Optional[str] = None,
        gcs_storage_base_dir: Optional[str] = None,
        gcs_results_bucket: Optional[str] = None,
        gcs_results_base_dir: Optional[str] = None,
        jaeger_tracing: Optional[bool] = False,
        jaeger_agent_hostname: Optional[str] = "jaeger",
        jaeger_agent_port: Optional[int] = 6831,
        gcp_tracing: Optional[bool] = False,
    ):

        # TODO: validation lol

        self.debug = debug
        self.port = port

        # local:s3:gcs:audius
        self.audio_path = audio_path

        # local | gcs | s3
        self.output_location = output_location

        if (
            "local" in self.audio_path.split(":")
            and local_storage_base_dir is None
        ):
            raise CyberpunkConfigException(
                "local_storage_base_dir must be configured if `local` in audio_path",
            )

        self.local_storage_base_dir = local_storage_base_dir

        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", None)
        self.aws_secret_access_key = os.environ.get(
            "AWS_SECRET_ACCESS_KEY",
            None,
        )
        self.aws_region = os.environ.get("AWS_REGION", None)

        if "s3" in self.audio_path.split(":"):

            if (
                self.aws_access_key_id is None
                or self.aws_secret_access_key is None
                or self.aws_region is None
            ):
                raise CyberpunkConfigException(
                    "to use s3 as an audio store, the aws access key id, aws secret access key, and aws region must be "
                    "provided ",
                )

            if s3_storage_bucket is None:
                raise CyberpunkConfigException(
                    "s3_storage_bucket must be configured if `s3` in audio_path",
                )

        # self.s3_loader_bucket = s3_loader_bucket
        # self.s3_loader_base_dir = s3_loader_base_dir

        self.s3_storage_bucket = s3_storage_bucket
        self.s3_storage_base_dir = s3_storage_base_dir

        self.s3_results_bucket = s3_results_bucket
        self.s3_results_base_dir = s3_results_base_dir

        if "gcs" in self.audio_path.split(":"):
            if gcs_storage_bucket is None:
                raise CyberpunkConfigException(
                    "gcs_storage_bucket must be configured if `gcs` in audio_path",
                )
            if google_application_credentials is None:
                raise CyberpunkConfigException(
                    "google_application_credentials must be configured if `gcs` in audio_path",
                )

        self.google_application_credentials = google_application_credentials
        # self.gcs_loader_bucket = gcs_loader_bucket
        # self.gcs_loader_base_dir = gcs_loader_base_dir
        self.gcs_storage_bucket = gcs_storage_bucket
        self.gcs_storage_base_dir = gcs_storage_base_dir
        self.gcs_results_bucket = gcs_results_bucket
        self.gcs_results_base_dir = gcs_results_base_dir

        self.jaeger_tracing = jaeger_tracing
        self.jaeger_agent_hostname = jaeger_agent_hostname
        self.jaeger_agent_port = jaeger_agent_port

        self.gcp_tracing = gcp_tracing

    def __repr__(self):
        return (
            f"CyberpunkConfig ( "
            f"audio_path: {self.audio_path}, "
            f"output_location: {self.output_location}, "
            f"local_storage_base_dir: {self.local_storage_base_dir}, "
            f")"
        )


_CYBERPUNK_CONFIG: Optional[CyberpunkConfig] = None


def configure_config(provided_config: Optional[CyberpunkConfig] = None):
    global _CYBERPUNK_CONFIG

    if provided_config is not None:
        _CYBERPUNK_CONFIG = provided_config
    else:
        _CYBERPUNK_CONFIG = CyberpunkConfig(
            debug=True,
            port=8080,
            output_location=os.environ.get("OUTPUT_LOCATION", "local"),
            audio_path=os.environ.get("AUDIO_PATH", "local"),
            local_storage_base_dir=os.environ.get(
                "LOCAL_STORAGE_BASE_DIR",
                "testdata/",
            ),
            # s3_loader_bucket=os.environ.get("S3_LOADER_BUCKET", None),
            # s3_loader_base_dir=os.environ.get("S3_LOADER_BASE_DIR", None),
            s3_storage_bucket=os.environ.get("S3_STORAGE_BUCKET", None),
            s3_results_bucket=os.environ.get("S3_RESULTS_BUCKET", None),
            s3_results_base_dir=os.environ.get("S3_RESULTS_BASE_DIR", None),
            google_application_credentials=os.environ.get(
                "GOOGLE_APPLICATION_CREDENTIALS",
                None,
            ),
            # gcs_loader_bucket=os.environ.get("GCS_LOADER_BUCKET", None),
            # gcs_loader_base_dir=os.environ.get("GCS_LOADER_BASE_DIR", None),
            gcs_storage_bucket=os.environ.get("GCS_STORAGE_BUCKET", None),
            gcs_storage_base_dir=os.environ.get("GCS_STORAGE_BASE_DIR", None),
            gcs_results_bucket=os.environ.get("GCS_RESULTS_BUCKET", None),
            gcs_results_base_dir=os.environ.get("GCS_RESULTS_BASE_DIR", None),
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
