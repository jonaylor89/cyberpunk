import logging
import os
from functools import lru_cache
from typing import Tuple

from google.cloud import storage
from pydub import AudioSegment

from cyberpunk.config import get_config

MAX_CACHE_SIZE = 50


class GCSStorageException(Exception):
    pass


class GCSStorage:
    def __init__(self):
        config = get_config()

        self.google_application_credentials = os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS",
        )

        if self.google_application_credentials is None:
            raise GCSStorageException(
                "to use gcs as an audio store, the google application credential's path must be provided ",
            )

        self.gcs = storage.Client.from_service_account_json(
            self.google_application_credentials,
        )

        self.gcs_loader_bucket = config.gcs_loader_bucket
        self.gcs_loader_base_dir = config.gcs_loader_base_dir

        self.gcs_storage_bucket = config.gcs_storage_bucket
        self.gcs_storage_base_dir = config.gcs_storage_base_dir

        self.gcs_results_bucket = config.gcs_results_bucket
        self.gcs_results_base_dir = config.gcs_results_base_dir

    def __contains__(self, element):
        return self.contains(element)

    def contains(self, key: str) -> bool:
        bucket = self.gcs.get_bucket(self.gcs_storage_bucket)
        blobs = list(
            self.gcs.list_blobs(
                bucket,
                prefix=f"{self.gcs_storage_base_dir}",
            ),
        )
        for blob in blobs:
            if blob == key:
                return True

        return False

    @lru_cache(MAX_CACHE_SIZE)
    def get_segment(self, key: str) -> Tuple[AudioSegment, str]:
        logging.info(f"pulling key from gcs: {key}")

        bucket = self.gcs.get_bucket(self.gcs_storage_bucket)
        blob = storage.Blob(f"{self.gcs_storage_base_dir}{key}", bucket)
        with open("f/tmp/{key}") as tmp:
            self.gcs.download_blob_to_file(
                blob,
                tmp,
            )

        segment = AudioSegment.from_file(f"/tmp/{key}")

        return segment, f"/tmp/{key}"

    def save_segment(self, segment: AudioSegment, key: str, file_type: str):
        logging.debug(f"exporting segment {key} to tmp dir")
        segment.export(
            f"/tmp/{key}",
            format=file_type,
        )

        bucket_name = (
            self.gcs_results_bucket
            if self.gcs_results_bucket is not None
            else self.gcs_storage_bucket
        )
        bucket = self.gcs.get_bucket(bucket_name)
        blob = bucket.blob(key)
        logging.info(
            f"uploaded {key} to results bucket {self.gcs_results_bucket}",
        )
        blob.upload_from_filename(
            f"tmp/{key}",
            content_type=f"audio/{file_type}",
        )
