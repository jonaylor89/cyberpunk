from dataclasses import dataclass

from pydub import AudioSegment

from cyberpunk.exceptions import (
    TransformationInputParseException,
    TransformationProcessException,
)
from cyberpunk.transformations import TransformationInput


@dataclass
class ReverseInput:

    reverse: bool

    @classmethod
    def from_str(cls, arg: str):
        try:
            if arg not in ["True", "true", "1", "yes", "Y", "y"]:
                return cls(reverse=False)
        except Exception as e:
            raise TransformationInputParseException(e)
        else:
            return cls(reverse=True)

    def __iter__(self):
        return "reverse", self.reverse

    def __str__(self) -> str:
        return f"{self.reverse}"


class Reverse:
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
            assert isinstance(inputs, ReverseInput)
            if inputs.reverse:
                reversed_segment = segment.reverse()
            else:
                reversed_segment = segment
        except Exception as e:
            raise TransformationProcessException(e)
        else:
            return reversed_segment
