from pydub import AudioSegment
from typing import Any, Dict, Tuple

from cyberpunk.transformations import (
    Transformation,
    Reverse,
    Repeat,
    Slice,
    Concat,
)
from cyberpunk.storage import audio_storage


def process_args(base_filename: str, args: Dict) -> Tuple[str, str]:

    lookup_table: Dict[str, Transformation] = {
        "reverse": Reverse(),
        "repeat": Repeat(),
        "slice": Slice(),
        "concat": Concat(),
    }

    # Create Audio Segment
    audio_segment: AudioSegment = audio_storage.get_segment(base_filename)

    # Pass Audio Segment through Each Stage
    for (k, v) in args.items():
        if k in lookup_table.keys():
            transformation: Transformation = lookup_table[k]
            assert transformation is not None

            inputs: Dict[str, Any] = transformation.parse_input_from_str(v)
            audio_segment = transformation.process(audio_segment, inputs)

    processed_filename = audio_storage.save_segment(base_filename, audio_segment)

    # Return Filename and Audio Type
    return processed_filename, "audio/mp3"


# TODO: This function should return the users input as json
# It'll help them debug
def parse_query(filename: str, args: Dict) -> Dict:
    return {
        "reverse": False,
        "repeat": 0,
        "slice": {
            "start": 0,
            "end": 0,
        },
    }
