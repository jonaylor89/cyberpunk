import logging

import boto3
from pydub import AudioSegment


class S3Storage(object):
    def __init__(self):
        self.s3 = boto3.resource("s3")

    def get_segment(self, key: str) -> AudioSegment:
        logging.info(f"pulling key from aws s3: {key}")

        return AudioSegment.empty()

    def save_segment(
        self,
        base_filename: str,
        segment: AudioSegment,
    ) -> str:
        # TODO: export with Filename unique to the stages run (for caching)
        # TODO: All for exporting different file type (e.g. mp3, wav, etc.)
        processed_filename = f"processed_{base_filename}"
        segment.export(f"tmp/{processed_filename}", format="mp3")

        return processed_filename
