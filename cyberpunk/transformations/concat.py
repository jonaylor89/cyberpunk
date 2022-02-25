from typing import Any, Dict

from pydub import AudioSegment

from cyberpunk.exceptions import (
    TransformationInputParseException,
    TransformationProcessException,
)
from cyberpunk.storage import get_storage


class Concat:
    def __call__(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        return self.process(segment, inputs)

    def parse_input_from_str(self, arg: str) -> Dict:
        other_filename = arg

        try:
            other_segment = get_storage().get_segment(other_filename)

        except Exception as e:
            raise TransformationInputParseException(e)
        else:
            return {
                "other": other_segment,
            }

    def process(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        try:
            other = inputs["other"]
            concated_segment = segment + other
        except Exception as e:
            raise TransformationProcessException(e)
        else:
            return concated_segment
