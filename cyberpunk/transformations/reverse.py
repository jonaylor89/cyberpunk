from typing import Any, Dict

from pydub import AudioSegment

from cyberpunk.exceptions import (
    TransformationInputParseException,
    TransformationProcessException,
)


class Reverse:
    def __call__(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        return self.process(segment, inputs)

    def parse_input_from_str(self, arg: str) -> Dict:

        try:
            if arg not in ["True", "true", "1", "yes", "Y", "y"]:
                return {"reverse": False}
        except Exception as e:
            raise TransformationInputParseException(e)
        else:
            return {"reverse": True}

    def process(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        try:
            if inputs["reverse"]:
                reversed_segment = segment.reverse()
            else:
                reversed_segment = segment
        except Exception as e:
            raise TransformationProcessException(e)
        else:
            return reversed_segment
