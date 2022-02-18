"""module for audio transformations"""

# nopycln: file

from typing import Any, Dict, Protocol

from pydub import AudioSegment

from cyberpunk.transformations.concat import Concat
from cyberpunk.transformations.fade_in import FadeIn
from cyberpunk.transformations.fade_out import FadeOut
from cyberpunk.transformations.repeat import Repeat
from cyberpunk.transformations.reverse import Reverse
from cyberpunk.transformations.slice import Slice


class Transformation(Protocol):
    def __call__(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        """runs the tranformation on the given AudioSegment and returns the output"""

    def parse_input_from_str(self, arg: str) -> Dict[str, Any]:
        """parses a string input proper inputs for that transformation"""

    def process(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        """runs the transformation on the given AudioSegment and returns the output"""
