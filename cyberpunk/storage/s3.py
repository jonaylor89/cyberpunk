import logging

import boto3
from pydub import AudioSegment

from cyberpunk.config import get_config


class S3Storage:
    def __init__(self):
        config = get_config()

        self.s3 = boto3.client("s3")
        self.s3_storage_bucket = config.s3_storage.s3_storage_bucket
        self.s3_storage_base_dir = config.s3_storage.s3_storage_base_dir

    def get_segment(self, key: str) -> AudioSegment:
        logging.info(f"pulling key from aws s3: {key}")

        self.s3.download_file(
            self.s3_storage_bucket,
            f"{self.s3_storage_base_dir}{key}",
            f"testdata/{key}",
        )

        segment = AudioSegment.from_file(f"testdata/{key}")

        return segment

    def save_segment(
        self,
        base_filename: str,
        segment: AudioSegment,
        file_format: str,
    ) -> str:
        # TODO: export with Filename unique to the stages run (for caching)
        processed_filename = f"processed_{base_filename}.{file_format}"
        segment.export(f"tmp/{processed_filename}", format=file_format)

        return processed_filename
