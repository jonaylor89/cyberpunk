import logging
from typing import Any, Dict

from pydub import AudioSegment


class Slice:
    def __call__(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        return self.process(segment, inputs)

    def parse_input_from_str(self, arg: str) -> Dict:
        # TODO: Slices can have no start (implied 0) or no end (implied length of segment)

        try:
            start_str, end_str = tuple(arg.split(":"))

            start = int(start_str)
            end = int(end_str)

        except Exception as e:
            logging.error(f"failure to parse input `{arg}` for `Slice` : {e}")

            return {}
        else:
            return {
                "start": start,
                "end": end,
            }

    def process(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:

        try:
            start = inputs["start"]
            end = inputs["end"]

            sliced_segment = segment[start:end]
        except Exception as e:
            logging.error(
                f"failure to process input `{inputs}` for `Slice` : {e}",
            )
            return AudioSegment.empty()
        else:
            return sliced_segment
