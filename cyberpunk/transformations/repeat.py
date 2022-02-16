from typing import Any, Dict

from pydub import AudioSegment


class Repeat(object):
    def __call__(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        return self.process(segment, inputs)

    def parse_input_from_str(self, arg: str) -> Dict[str, Any]:
        multiplier = int(arg)

        return {
            "multiplier": multiplier,
        }

    def process(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        multiplier = inputs["multiplier"]
        repeated_segment = segment * multiplier

        return repeated_segment
