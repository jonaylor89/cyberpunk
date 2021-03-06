from dataclasses import dataclass

from pydub import AudioSegment

from cyberpunk.exceptions import (
    TransformationInputParseException,
    TransformationProcessException,
)
from cyberpunk.transformations import TransformationInput


@dataclass
class FadeOutInput:

    duration: int

    @classmethod
    def from_str(cls, arg: str):
        try:
            duration = int(arg)
        except Exception as e:
            raise TransformationInputParseException(e)
        else:
            return cls(duration=duration)

    def __iter__(self):
        return "duration", self.duration

    def __str__(self):
        return f"{self.duration}"


class FadeOut:
    def __call__(
        self,
        segment: AudioSegment,
        inputs: TransformationInput,
    ) -> AudioSegment:
        return self.run(segment, inputs)

    def run(
        self,
        segment: AudioSegment,
        inputs: TransformationInput,
    ) -> AudioSegment:
        try:
            assert isinstance(inputs, FadeOutInput)
            faded_segment = segment.fade_out(inputs.duration)
        except Exception as e:
            raise TransformationProcessException(e)
        else:
            return faded_segment
