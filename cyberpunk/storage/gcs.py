import logging
import os
from typing import Tuple

from google.cloud import storage
from pydub import AudioSegment

from cyberpunk.config import get_config


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

        self.gcs = storage.Client()

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
