import logging
from typing import Any, Dict

from pydub import AudioSegment


class Repeat:
    def __call__(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        return self.process(segment, inputs)

    def parse_input_from_str(self, arg: str) -> Dict[str, Any]:
        try:
            multiplier = int(arg)
        except Exception as e:
            logging.error(f"failure to parse input `{arg}` for `Repeat` : {e}")

            return {}
        else:
            return {
                "multiplier": multiplier,
            }

    def process(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:

        try:
            multiplier = inputs["multiplier"]
            repeated_segment = segment * multiplier
        except Exception as e:
            logging.error(
                f"failure to process input `{inputs}` for `Repeat` : {e}",
            )
            return AudioSegment.empty()
        else:
            return repeated_segment
