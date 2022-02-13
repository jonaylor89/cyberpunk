
from pydub import AudioSegment
from typing import Dict, Any

from . import Transformation

class Repeat(object):

    def __init__(self):
        return

    def __call__(self, segment: AudioSegment, inputs: Dict[str, Any]) -> AudioSegment:
        return self.process(segment, inputs)

    @classmethod
    def parse_input_from_str(cls, arg: str) -> Dict[str, Any]:
        multiplier = int(arg)

        return {
            "multiplier": multiplier,
        }

    def process(self, segment: AudioSegment, inputs: Dict[str, Any]) -> AudioSegment:
        multiplier = inputs["multiplier"]
        repeated_segment = segment * multiplier

        return repeated_segment

