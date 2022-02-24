import logging
from typing import Any, Dict

from pydub import AudioSegment


class Reverse:
    def __call__(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        return self.process(segment, inputs)

    def parse_input_from_str(self, arg: str) -> Dict:
        return {}

    def process(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        try:
            reversed_segment = segment.reverse()
        except Exception as e:
            logging.error(
                f"failure to process input `{inputs}` for `Reverse` : {e}",
            )
            return AudioSegment.empty()
        else:
            return reversed_segment
