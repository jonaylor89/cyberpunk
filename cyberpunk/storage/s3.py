import logging
from typing import Dict, Tuple

import boto3
from pydub import AudioSegment

from cyberpunk.config import get_config


class S3Storage:
    def __init__(self):
        config = get_config()

        self.s3 = boto3.client("s3")

        self.s3_loader_bucket = config.s3_loader_bucket
        self.s3_loader_base_dir = config.s3_loader_base_dir

        self.s3_storage_bucket = config.s3_storage_bucket
        self.s3_storage_base_dir = config.s3_storage_base_dir

        self.s3_results_bucket = config.s3_results_bucket
        self.s3_results_base_dir = config.s3_results_base_dir

    def __contains__(self, element):
        return contains(element)

    def contains(self, key: str) -> bool:
        return False

    def get_segment(self, key: str) -> Tuple[AudioSegment, str]:
        logging.info(f"pulling key from aws s3: {key}")

        self.s3.download_file(
            self.s3_storage_bucket,
            f"{self.s3_storage_base_dir}{key}",
            f"testdata/{key}",
        )

        segment = AudioSegment.from_file(f"testdata/{key}")

        return segment, f"testdata/{key}"

    def get_stats(self) -> Dict:
        return {}
