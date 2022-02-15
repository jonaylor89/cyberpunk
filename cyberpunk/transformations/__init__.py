from pydub import AudioSegment
from typing import Protocol, Dict, Any

from cyberpunk.transformations.reverse import Reverse
from cyberpunk.transformations.repeat import Repeat
from cyberpunk.transformations.slice import Slice
from cyberpunk.transformations.concat import Concat


class Transformation(Protocol):
    def __call__(self, segment: AudioSegment, inputs: Dict[str, Any]) -> AudioSegment:
        """runs the tranformation on the given AudioSegment and returns the output"""

    def parse_input_from_str(self, arg: str) -> Dict[str, Any]:
        """parses a string input proper inputs for that transformation"""

    def process(self, segment: AudioSegment, inputs: Dict[str, Any]) -> AudioSegment:
        """runs the transformation on the given AudioSegment and returns the output"""
