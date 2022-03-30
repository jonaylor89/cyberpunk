import logging
import os
from functools import lru_cache
from typing import Tuple

import boto3
from botocore.exceptions import ClientError
from pydub import AudioSegment

from cyberpunk.config import get_config

MAX_CACHE_SIZE = 50


class S3StorageException(Exception):
    pass


class S3Storage:
    def __init__(self):
        config = get_config()

        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.environ.get("AWS_REGION")

        if (
            self.aws_access_key_id is None
            or self.aws_secret_access_key is None
            or self.aws_region is None
        ):
            raise S3StorageException(
                "to use s3 as an audio store, the aws access key id, aws secret access key, and aws region must be "
                "provided ",
            )

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

        self.s3_loader_bucket = config.s3_loader_bucket
        self.s3_loader_base_dir = config.s3_loader_base_dir

        self.s3_storage_bucket = config.s3_storage_bucket
        self.s3_storage_base_dir = config.s3_storage_base_dir

        self.s3_results_bucket = config.s3_results_bucket
        self.s3_results_base_dir = config.s3_results_base_dir

    def __contains__(self, element):
        return self.contains(element)

    def contains(self, key: str) -> bool:
        response = self.s3.list_objects_v2(
            Bucket=self.s3_storage_bucket,
            Prefix=f"{self.s3_storage_base_dir}{key}",
        )
        for obj in response.get("Contents", []):
            if obj["Key"] == key:
                return True

        return False

    @lru_cache(MAX_CACHE_SIZE)
    def get_segment(self, key: str) -> Tuple[AudioSegment, str]:
        logging.info(f"pulling key from aws s3: {key}")

        self.s3.download_file(
            self.s3_storage_bucket,
            f"{self.s3_storage_base_dir}{key}",
            f"/tmp/{key}",
        )

        segment = AudioSegment.from_file(f"/tmp/{key}")

        return segment, f"/tmp/{key}"

    def save_segment(self, segment: AudioSegment, key: str, file_type: str):
        """
        Upload a file to an S3 bucket
        """
        segment.export(
            f"/tmp/{key}",
            format=file_type,
        )

        object_name = f"{self.s3_results_base_dir if self.s3_results_base_dir is not None else self.s3_storage_base_dir}{key}"

        # Upload the file
        bucket = (
            self.s3_results_bucket
            if self.s3_results_bucket is not None
            else self.s3_storage_bucket
        )
        try:
            response = self.s3.upload_file(f"/tmp/{key}", bucket, key)
        except ClientError as e:
            logging.error(e)
