import logging
from typing import Generator

from flask import Response, redirect, stream_with_context

from cyberpunk.config import get_config


def stream_audio_file(filename: str, chunk_size: int = 4096) -> Generator:
    with open(f"/tmp/{filename}", "rb") as faudio:
        data = faudio.read(chunk_size)
        while data:
            yield data
            data = faudio.read(chunk_size)


def build_local_stream(processed_file, file_type):
    return Response(
        stream_with_context(stream_audio_file(processed_file)),
        mimetype=file_type,
    )


def build_presigned_s3_url():
    return "https://example.com"


def build_presigned_gcs_url():
    return "https://example.com"


def build_response(processed_file, file_type):
    config = get_config()
    if config.gcs_results_bucket is None and config.s3_storage_bucket is None:
        return build_local_stream(processed_file, file_type)
    elif config.gcs_results_bucket is not None:
        url = build_presigned_gcs_url()
        return redirect(url, 301)
    elif config.s3_storage_bucket is not None:
        url = build_presigned_s3_url()
        return redirect(url, 301)
    else:
        logging.error("que?")
