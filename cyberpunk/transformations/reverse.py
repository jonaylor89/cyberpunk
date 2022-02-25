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

        try:
            if arg not in ["True", "true", "1", "yes", "Y", "y"]:
                return {"reverse": False}
        except Exception as e:
            logging.error(
                f"failure to parse input `{arg}` for `Reverse` : {e}",
            )

            return {}
        else:
            return {"reverse": True}

    def process(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        try:
            if inputs["reverse"]:
                reversed_segment = segment.reverse()
            else:
                reversed_segment = segment
        except Exception as e:
            logging.error(
                f"failure to process input `{inputs}` for `Reverse` : {e}",
            )
            return AudioSegment.empty()
        else:
            return reversed_segment
