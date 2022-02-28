from dataclasses import dataclass
from typing import Optional

from pydub import AudioSegment

from cyberpunk.exceptions import (
    TransformationInputParseException,
    TransformationProcessException,
)
from cyberpunk.transformations import TransformationInput


@dataclass
class SliceInput:

    start: Optional[int]
    end: Optional[int]

    @classmethod
    def from_str(cls, arg: str):

        try:
            start_str, end_str = tuple(arg.split(":"))

            start = int(start_str) if start_str != "" else None
            end = int(end_str) if end_str != "" else None

        except Exception as e:
            raise TransformationInputParseException(e)
        else:
            return SliceInput(
                start=start,
                end=end,
            )

    def __iter__(self):
        yield "start", self.start
        yield "end", self.end

    def __str__(self):
        return f"{self.start if self.start is not None else ''}:{self.end if self.end is not None else ''}"


class Slice:
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
            assert isinstance(inputs, SliceInput)
            start = inputs.start
            end = inputs.end

            if start is None and end is None:
                raise TransformationProcessException(
                    "the start and end of a slice can't both be None",
                )

            if start is None:
                sliced_segment = segment[:end]
            elif end is None:
                sliced_segment = segment[start:]
            else:
                sliced_segment = segment[start:end]
        except Exception as e:
            raise TransformationProcessException(e)

        else:
            return sliced_segment
