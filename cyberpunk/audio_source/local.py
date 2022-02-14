from os import listdir
from os.path import isfile, join

from pydub import AudioSegment


class LocalStorage(object):
    def __init__(self):
        self.base_dir = "testdata/"
        self.results_dir = "processed/"

    def get_segment(self, key: str) -> AudioSegment:
        audio_segment: AudioSegment = AudioSegment.from_file(f"{self.base_dir}{key}")

        return audio_segment

    def save_segment(
        self,
        base_filename: str,
        segment: AudioSegment,
        save_results=False,
    ):
        # TODO: export with Filename unique to the stages run (for caching)
        # TODO: All for exporting different file type (e.g. mp3, wav, etc.)
        processed_filename = f"processed_{base_filename}"
        segment.export(f"{self.base_dir}{processed_filename}", format="mp3")

        if save_results:
            segment.export(f"{self.base_dir}{self.results_dir}{processed_filename}")
