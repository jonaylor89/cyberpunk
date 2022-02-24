import logging
from typing import Any, Dict

from pydub import AudioSegment


class FadeOut:
    def __call__(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        return self.process(segment, inputs)

    def parse_input_from_str(self, arg: str) -> Dict:
        try:
            duration = int(arg)
        except Exception as e:
            logging.error(
                f"failure to parse input `{arg}` for `FadeOut` : {e}",
            )

            return {}
        else:
            return {
                "duration": duration,
            }

    def process(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        try:
            duration = inputs["duration"]
            faded_segment = segment.fade_out(duration)
        except Exception as e:
            logging.error(
                f"failure to process input `{inputs}` for `FadeOut` : {e}",
            )
            return AudioSegment.empty()
        else:
            return faded_segment
