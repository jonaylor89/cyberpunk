from pydub import AudioSegment
from typing import Dict, Any


class Slice(object):
    def __call__(self, segment: AudioSegment, inputs: Dict[str, Any]) -> AudioSegment:
        return self.process(segment, inputs)

    def parse_input_from_str(self, arg: str) -> Dict:
        # TODO: Slices can have no start (implied 0) or no end (implied length of segment)

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
