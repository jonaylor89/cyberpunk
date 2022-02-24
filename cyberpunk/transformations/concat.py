import logging
from typing import Any, Dict

from pydub import AudioSegment

from cyberpunk.storage import get_storage


class Concat:
    def __call__(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        return self.process(segment, inputs)

    def parse_input_from_str(self, arg: str) -> Dict:
        other_filename = arg

        try:
            other_segment = get_storage().get_segment(other_filename)

        except Exception as e:
            logging.error(f"failure to parse input `{arg}` for `Concat` : {e}")

            return {}
        else:
            return {
                "other": other_segment,
            }

    def process(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        other = inputs["other"]
        concated_segment = segment + other

        return concated_segment
