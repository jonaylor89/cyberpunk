from typing import Any, Dict

from pydub import AudioSegment

from cyberpunk.exceptions import (
    TransformationInputParseException,
    TransformationProcessException,
)


class FadeIn:
    def __call__(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        return self.process(segment, inputs)

    def parse_input_from_str(self, arg: str) -> Dict:
        try:
            duration = int(arg)
        except Exception as e:
            raise TransformationInputParseException(e)
        else:
            return {
                "duration": duration,
            }

    def process(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        try:
            duration = inputs["duration"]
            faded_segment = segment.fade_in(duration)

        except Exception as e:
            raise TransformationProcessException(e)
        else:
            return faded_segment
