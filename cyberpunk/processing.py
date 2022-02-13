from pydub import AudioSegment
from typing import Any, Dict, Tuple, Type

from .transformations import Transformation, Reverse, Repeat, Slice


def process_args(base_filename: str, args: Dict) -> Tuple[str, str]:

    lookup_table: Dict[str, Transformation] = {
        "reverse": Reverse(),
        "repeat": Repeat(),
        "slice": Slice(),
    }

    # Create Audio Segment
    audio_segment: AudioSegment = AudioSegment.from_file(f"testdata/{base_filename}")

    # Pass Audio Segment through Each Stage
    for (k, v) in args.items():
        print(f"{k} = {v}")

        if k in lookup_table.keys():
            transformation: Transformation = lookup_table[k]
            assert transformation is not None

            inputs: Dict[str, Any] = transformation.parse_input_from_str(v)
            audio_segment = transformation.process(audio_segment, inputs)

    # TODO: export with Filename unique to the stages run (for caching)
    # TODO: All for exporting different file type (e.g. mp3, wav, etc.)
    processed_filename = f"processed_{base_filename}"
    audio_segment.export(f"testdata/{processed_filename}", format="mp3")

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

