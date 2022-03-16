#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

import click

from cyberpunk import __version__
from cyberpunk.config import CyberpunkConfig
from cyberpunk.server import create_app

app = create_app()


@click.command()
@click.version_option(__version__)
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
    "--local-storage-base-dir",
    default=lambda: os.environ.get("LOCAL_STORAGE_BASE_DIR", "testdata/"),
    help="Local directory contains the audio library",
)
@click.option(
    "--local-results-base-dir",
    default=lambda: os.environ.get("LOCAL_RESULTS_BASE_DIR", None),
    help="Local directory where processed audio files will be stored",
)
@click.option(
    "--s3-loader-bucket",
    default=lambda: os.environ.get("S3_LOADER_BUCKET", None),
    help="S3 bucket containing audio needing to be pre-loaded",
)
@click.option(
    "--s3-loader-base-dir",
    default=lambda: os.environ.get("S3_LOADER_BASE_DIR", None),
    help="Prefix in loader s3 bucket where the audio files are located",
)
@click.option(
    "--s3-storage-bucket",
    default=lambda: os.environ.get("S3_STORAGE_BUCKET", None),
    help="S3 bucket containing the audio files to be processed",
)
@click.option(
    "--s3-storage-base-dir",
    default=lambda: os.environ.get("S3_STORAGE_BASE_DIR", None),
    help="Prefix in storage s3 bucket where the audio files are located",
)
@click.option(
    "--s3-results-bucket",
    default=lambda: os.environ.get("S3_RESULTS_BUCKET", None),
    help="S3 bucket where the processed audio is stored",
)
@click.option(
    "--s3-results-base-dir",
    default=lambda: os.environ.get("S3_RESULTS_BASE_DIR", None),
    help="Prefix in results s3 bucket where the audio files should be stored",
)
def main(
    debug,
    port,
    cyberpunk_secret,
    audio_path,
    local_storage_base_dir,
    local_results_base_dir,
    s3_loader_bucket,
    s3_loader_base_dir,
    s3_storage_bucket,
    s3_storage_base_dir,
    s3_results_bucket,
    s3_results_base_dir,
):

    print(cyberpunk_secret)

    config = CyberpunkConfig(
        audio_path=audio_path,
        local_storage_base_dir=local_storage_base_dir,
        local_results_base_dir=local_results_base_dir,
        s3_loader_bucket=s3_loader_bucket,
        s3_loader_base_dir=s3_loader_base_dir,
        s3_storage_bucket=s3_storage_bucket,
        s3_storage_base_dir=s3_storage_base_dir,
        s3_results_bucket=s3_results_bucket,
        s3_results_base_dir=s3_results_base_dir,
    )

    logging.debug(f"running server with config: {config}")

    server = create_app(config)
    server.run(
        debug=debug,
        load_dotenv=True,
        port=port,
    )


if __name__ == "__main__":
    main()
