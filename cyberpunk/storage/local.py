import logging

from pydub import AudioSegment


class LocalStorage:
    def __init__(self):
        self.base_dir = "testdata/"

    def get_segment(self, key: str) -> AudioSegment:
        logging.info(f"pulling key from local storage: {key}")
        audio_segment: AudioSegment = AudioSegment.from_file(
            f"{self.base_dir}{key}",
        )

        return audio_segment

    def save_segment(
        self,
        base_filename: str,
        segment: AudioSegment,
        file_format: str,
    ) -> str:
        # TODO: export with Filename unique to the stages run (for caching)
        processed_filename = f"processed_{base_filename}.{file_format}"
        segment.export(
            f"{self.base_dir}{processed_filename}",
            format=file_format,
        )

        return processed_filename
