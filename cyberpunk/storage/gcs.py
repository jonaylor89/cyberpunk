import logging
from functools import lru_cache
from typing import Optional, Tuple

from google.cloud import storage
from pydub import AudioSegment

from cyberpunk.config import get_config

MAX_CACHE_SIZE = 50


class GCSStorageException(Exception):
    pass


class GCSStorage:
    def __init__(self):
        config = get_config()

        self.google_application_credentials = (
            config.google_application_credentials
        )

        self.gcs = storage.Client.from_service_account_json(
            self.google_application_credentials,
        )

        # self.gcs_loader_bucket = config.gcs_loader_bucket
        # self.gcs_loader_base_dir = config.gcs_loader_base_dir

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
    def get_segment(
        self,
        key: str,
        full_path=False,
    ) -> Tuple[AudioSegment, str]:
        logging.info(f"pulling key from gcs: {key}")

        if full_path:

            # extract bucket name by splitting string by '/'
            # take the 3rd item in the list (index position 2) which is the bucket name
            bucket = key.split("/")[2]

            # extract file name by splitting string to remove gs:// prefix and bucket name
            # rejoin to rebuild the file path
            object_name = "/".join(key.split("/")[3:])

            ext = object_name.split(".")[-1]

            bucket = self.gcs.get_bucket(bucket)
            blob = storage.Blob(object_name, bucket)
            location: str = f"remote-audio.{ext}"
            with open("f/tmp/{location}") as tmp:
                self.gcs.download_blob_to_file(
                    blob,
                    tmp,
                )

            segment = AudioSegment.from_file(f"/tmp/{location}")

        else:
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


# GCS Singletons
_GCS_STORAGE: Optional[GCSStorage] = None


def configure_gcs_storage():
    global _GCS_STORAGE

    logging.info(f"configuring gcs store")

    _GCS_STORAGE = GCSStorage()


def get_gcs_storage() -> GCSStorage:
    global _GCS_STORAGE

    if _GCS_STORAGE is None:
        configure_gcs_storage()

    assert _GCS_STORAGE is not None
    return _GCS_STORAGE
