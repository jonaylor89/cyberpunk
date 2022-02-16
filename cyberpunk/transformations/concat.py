from pydub import AudioSegment
from typing import Dict, Any

from cyberpunk.storage import audio_storage


class Concat(object):
    def __call__(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        return self.process(segment, inputs)

    def parse_input_from_str(self, arg: str) -> Dict:
        other_filename = arg
        other_segment = audio_storage.get_segment(other_filename)

        return {
            "other": other_segment,
        }

    def process(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        other = inputs["other"]
        concated_segment = segment + other

        return concated_segment
