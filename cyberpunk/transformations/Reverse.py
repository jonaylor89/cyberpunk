
from pydub import AudioSegment
from typing import Dict, Any

from . import Transformation

class Reverse(object):

    def __init__(self):
        return

    def __call__(self, segment: AudioSegment, inputs: Dict[str, Any]) -> AudioSegment:
        return self.process(segment, inputs)

    @classmethod
    def parse_input_from_str(cls, arg: str) -> Dict:
        return {}

    def process(self, segment: AudioSegment, inputs: Dict[str, Any]) -> AudioSegment:
        reversed_segment = segment.reverse()

        return reversed_segment



