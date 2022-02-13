
from pydub import AudioSegment
from typing import Dict, Any

from . import Transformation

class Slice(object):

    def __init__(self):
        return

    def __call__(self, segment: AudioSegment, inputs: Dict[str, Any]) -> AudioSegment:
        return self.process(segment, inputs)

    @classmethod
    def parse_input_from_str(cls, arg: str) -> Dict:
        start_str, end_str = tuple(arg.split(":"))

        start = int(start_str)
        end = int(end_str)

        return {
            "start": start,
            "end": end,
        }


    def process(self, segment: AudioSegment, inputs: Dict[str, Any]) -> AudioSegment:
        start = inputs["start"]
        end = inputs["end"]

        sliced_segment = segment[start:end]
        return sliced_segment
