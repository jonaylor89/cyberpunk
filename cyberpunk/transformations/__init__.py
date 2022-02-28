"""module for audio transformations"""

# nopycln: file
from typing import Protocol

from pydub import AudioSegment


class TransformationInput(Protocol):
    @classmethod
    def from_str(cls, arg: str):
        """serialize input from string"""

    def __iter__(self):
        """convert to iterable"""

    def __str__(self) -> str:
        """deserialize input to string"""


class Transformation(Protocol):
    def __call__(
        self,
        segment: AudioSegment,
        inputs: TransformationInput,
    ) -> AudioSegment:
        """runs the transformation on the given AudioSegment and returns the output"""

    def run(
        self,
        segment: AudioSegment,
        inputs: TransformationInput,
    ) -> AudioSegment:
        """runs the transformation on the given AudioSegment and returns the output"""
