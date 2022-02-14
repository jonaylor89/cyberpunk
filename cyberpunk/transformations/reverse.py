from pydub import AudioSegment
from typing import Dict, Any


class Reverse(object):
    def __call__(self, segment: AudioSegment, inputs: Dict[str, Any]) -> AudioSegment:
        return self.process(segment, inputs)

    def parse_input_from_str(self, arg: str) -> Dict:
        return {}

    def process(self, segment: AudioSegment, inputs: Dict[str, Any]) -> AudioSegment:
        reversed_segment = segment.reverse()

        return reversed_segment
