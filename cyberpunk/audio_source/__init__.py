from pydub import AudioSegment

from audio_source.local import LocalStorage


class AudioSource(object):
    def __init__(self):
        self.source = LocalStorage()

    def get_segment(self, key: str) -> AudioSegment:
        return self.source(key)

    def save_segment(self, base_filename: str, segment: AudioSegment) -> str:
        return self.source(base_filename, segment)
