from dataclasses import dataclass

from pydub import AudioSegment

from cyberpunk.exceptions import (
    TransformationInputParseException,
    TransformationProcessException,
)
from cyberpunk.transformations import TransformationInput


@dataclass
class RepeatInput:

    multiplier: int

    @classmethod
    def from_str(cls, arg: str):
        try:
            multiplier = int(arg)
        except Exception as e:
            raise TransformationInputParseException(e)
        else:
            return cls(multiplier=multiplier)

    def __iter__(self):
        return "multiplier", self.multiplier

    def __str__(self):
        return f"{self.multiplier}"


class Repeat:
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
            assert isinstance(inputs, RepeatInput)
            repeated_segment = segment * inputs.multiplier
        except Exception as e:
            raise TransformationProcessException(e)
        else:
            return repeated_segment
