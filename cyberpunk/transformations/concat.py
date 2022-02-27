from dataclasses import dataclass

from pydub import AudioSegment

from cyberpunk.exceptions import (
    TransformationInputParseException,
    TransformationProcessException,
)
from cyberpunk.storage import get_storage
from cyberpunk.transformations import TransformationInput


@dataclass
class ConcatInput:

    other: AudioSegment
    other_key: str

    @classmethod
    def from_str(cls, arg: str):
        other_filename = arg
        try:
            other_segment, other_key = get_storage().get_segment(
                other_filename,
            )
        except Exception as e:
            raise TransformationInputParseException(e)
        else:
            return cls(other=other_segment, other_key=other_key)

    def __iter__(self):
        return "other", self.other_key

    def __str__(self):
        return f"{self.other_key}"


class Concat:
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
            assert isinstance(inputs, ConcatInput)
            concated_segment = segment + inputs.other
        except Exception as e:
            raise TransformationProcessException(e)
        else:
            return concated_segment
