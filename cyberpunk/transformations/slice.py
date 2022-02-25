import logging
from typing import Any, Dict, Optional

from pydub import AudioSegment


class Slice:
    def __call__(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        return self.process(segment, inputs)

    def parse_input_from_str(self, arg: str) -> Dict[str, Optional[int]]:

        try:
            start_str, end_str = tuple(arg.split(":"))

            start = int(start_str) if start_str != "" else None
            end = int(end_str) if end_str != "" else None

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

            if start is None:
                sliced_segment = segment[:end]
            elif end is None:
                sliced_segment = segment[start:]
            else:
                sliced_segment = segment[start:end]
        except Exception as e:
            logging.error(
                f"failure to process input `{inputs}` for `Slice` : {e}",
            )
            return AudioSegment.empty()
        else:
            return sliced_segment
