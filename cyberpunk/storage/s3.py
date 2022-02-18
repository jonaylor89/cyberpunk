import logging

import boto3
from pydub import AudioSegment


class S3Storage:
    def __init__(self):
        self.s3 = boto3.resource("s3")

    def get_segment(self, key: str) -> AudioSegment:
        logging.info(f"pulling key from aws s3: {key}")

        return AudioSegment.empty()

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
