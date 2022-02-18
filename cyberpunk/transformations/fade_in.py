from typing import Any, Dict

from pydub import AudioSegment


class FadeIn:
    def __call__(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        return self.process(segment, inputs)

    def parse_input_from_str(self, arg: str) -> Dict:
        duration = int(arg)
        return {
            "duration": duration,
        }

    def process(
        self,
        segment: AudioSegment,
        inputs: Dict[str, Any],
    ) -> AudioSegment:
        duration = inputs["duration"]
        faded_segment = segment.fade_in(duration)

        return faded_segment
