#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

import click

from cyberpunk import __version__
from cyberpunk.config import CyberpunkConfig
from cyberpunk.server import create_app

app = create_app()


@click.group()
@click.version_option(__version__)
def cli():
    return


@cli.command()
@click.option(
    "-D",
    "--debug",
    is_flag=True,
    help="enables debug mode",
)
@click.option(
    "--port",
    type=click.INT,
    default=lambda: os.environ.get("PORT", 8080),
    help="Server port number",
)
@click.option(
    "--cyberpunk-secret",
    default=lambda: os.environ.get("CYBERPUNK_SECRET", "mysecret"),
    help="Secret used for the URL signature",
)
@click.option(
    "--audio-path",
    default=lambda: os.environ.get("AUDIO_PATH", "local"),
    help="Sources for audio files and in which order to search for them",
)
@click.option(
    "--output-location",
    default=lambda: os.environ.get("OUTPUT_LOCATION", "local"),
    help="The output location for the processed audio files",
)
@click.option(
    "--local-storage-base-dir",
    default=lambda: os.environ.get("LOCAL_STORAGE_BASE_DIR", "testdata/"),
    help="Local directory contains the audio library",
)
# @click.option(
#     "--s3-loader-bucket",
#     default=lambda: os.environ.get("S3_LOADER_BUCKET", None),
#     help="S3 bucket containing audio needing to be pre-loaded",
# )
# @click.option(
#     "--s3-loader-base-dir",
#     default=lambda: os.environ.get("S3_LOADER_BASE_DIR", ""),
#     help="Prefix in loader s3 bucket where the audio files are located",
# )
@click.option(
    "--s3-storage-bucket",
    default=lambda: os.environ.get("S3_STORAGE_BUCKET", None),
    help="S3 bucket containing the audio files to be processed",
)
@click.option(
    "--s3-storage-base-dir",
    default=lambda: os.environ.get("S3_STORAGE_BASE_DIR", ""),
    help="Prefix in storage s3 bucket where the audio files are located",
)
@click.option(
    "--s3-results-bucket",
    default=lambda: os.environ.get("S3_RESULTS_BUCKET", None),
    help="S3 bucket where the processed audio is stored",
)
@click.option(
    "--s3-results-base-dir",
    default=lambda: os.environ.get("S3_RESULTS_BASE_DIR", ""),
    help="Prefix in results s3 bucket where the audio files should be stored",
)
@click.option(
    "--google_application_credentials",
    default=lambda: os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None),
    help="Google Cloud service account credentials path",
)
# @click.option(
#     "--gcs-loader-bucket",
#     default=lambda: os.environ.get("GCS_LOADER_BUCKET", None),
#     help="GCS bucket containing audio needing to be pre-loaded",
# )
# @click.option(
#     "--gcs-loader-base-dir",
#     default=lambda: os.environ.get("GCS_LOADER_BASE_DIR", ""),
#     help="Prefix in loader gcs bucket where the audio files are located",
# )
@click.option(
    "--gcs-storage-bucket",
    default=lambda: os.environ.get("GCS_STORAGE_BUCKET", None),
    help="GCS bucket containing the audio files to be processed",
)
@click.option(
    "--gcs-storage-base-dir",
    default=lambda: os.environ.get("GCS_STORAGE_BASE_DIR", ""),
    help="Prefix in storage gcs bucket where the audio files are located",
)
@click.option(
    "--gcs-results-bucket",
    default=lambda: os.environ.get("GCS_RESULTS_BUCKET", None),
    help="GCS bucket where the processed audio is stored",
)
@click.option(
    "--gcs-results-base-dir",
    default=lambda: os.environ.get("GCS_RESULTS_BASE_DIR", ""),
    help="Prefix in results GCS bucket where the audio files should be stored",
)
@click.option(
    "--jaeger-tracing",
    is_flag=True,
    default=lambda: os.environ.get("JAEGER_TRACING_ENABLED", "0").lower()
    in ("true", "t", "1"),
    help="Export traces to Jaeger",
)
@click.option(
    "--jaeger-agent-hostname",
    default=lambda: os.environ.get("JAEGER_AGENT_HOSTNAME", "jaeger"),
    help="Hostname for Jaeger service",
)
@click.option(
    "--jaeger-agent-port",
    type=click.INT,
    default=lambda: os.environ.get("JAEGER_AGENT_PORT", 6831),
    help="Port for Jaeger service",
)
@click.option(
    "--gcp-tracing",
    is_flag=True,
    default=lambda: os.environ.get("GCP_TRACING_ENABLED", "0").lower()
    in ("true", "t", "0"),
    help="Export traces to Google Cloud Platform",
)
def serve(
    debug,
    port,
    cyberpunk_secret,
    audio_path,
    output_location,
    local_storage_base_dir,
    # s3_loader_bucket,
    # s3_loader_base_dir,
    s3_storage_bucket,
    s3_storage_base_dir,
    s3_results_bucket,
    s3_results_base_dir,
    google_application_credentials,
    # gcs_loader_bucket,
    # gcs_loader_base_dir,
    gcs_storage_bucket,
    gcs_storage_base_dir,
    gcs_results_bucket,
    gcs_results_base_dir,
    jaeger_tracing,
    jaeger_agent_hostname,
    jaeger_agent_port,
    gcp_tracing,
):

    print(cyberpunk_secret)

    config = CyberpunkConfig(
        debug=debug,
        port=port,
        audio_path=audio_path,
        output_location=output_location,
        local_storage_base_dir=local_storage_base_dir,
        # s3_loader_bucket=s3_loader_bucket,
        # s3_loader_base_dir=s3_loader_base_dir,
        s3_storage_bucket=s3_storage_bucket,
        s3_storage_base_dir=s3_storage_base_dir,
        s3_results_bucket=s3_results_bucket,
        s3_results_base_dir=s3_results_base_dir,
        google_application_credentials=google_application_credentials,
        # gcs_loader_bucket=gcs_loader_bucket,
        # gcs_loader_base_dir=gcs_loader_base_dir,
        gcs_storage_bucket=gcs_storage_bucket,
        gcs_storage_base_dir=gcs_storage_base_dir,
        gcs_results_bucket=gcs_results_bucket,
        gcs_results_base_dir=gcs_results_base_dir,
        jaeger_tracing=jaeger_tracing,
        jaeger_agent_hostname=jaeger_agent_hostname,
        jaeger_agent_port=jaeger_agent_port,
        gcp_tracing=gcp_tracing,
    )

    logging.debug(f"running server with config: {config}")

    server = create_app(config)
    server.run(
        debug=config.debug,
        load_dotenv=True,
        port=config.port,
    )


if __name__ == "__main__":
    cli()
