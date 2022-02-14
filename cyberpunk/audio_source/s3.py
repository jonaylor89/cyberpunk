import boto3
from pydub import AudioSegment


class S3Storage(object):

    def __init__(self):
        self.s3 = boto3.resource("s3")

    def get_segment(self, key: str) -> AudioSegment:
        pass

    def save_segment(self, base_filename: str, segment: AudioSegment):
        pass