from pydub import AudioSegment
from typing import Any, Dict, Tuple, Callable


def process_args(base_filename: str, args: Dict) -> Tuple[str, str]:

    lookup_table: Dict[str, Dict[str, Callable]] = {
        "reverse": {
            "parser": parse_reverse_segment_input,
            "processor": reverse_segment,
        },
        "repeat": {
            "parser": parse_repeat_segement_input,
            "processor": repeat_segment,
        },
        "slice": {
            "parser": parse_slice_segement_input,
            "processor": slice_segment,
        },
    }

    # Create Audio Segment
    audio_segment = AudioSegment.from_file(f"testdata/{base_filename}")

    # Pass Audio Segment through Each Stage
    for (k, v) in args.items():
        print(f"{k} = {v}")

        if k in lookup_table.keys():
            inputs = lookup_table[k]["parser"](v)
            audio_segment = lookup_table[k]["processor"](audio_segment, inputs)

    # TODO: export with Filename unique to the stages run (for caching)
    # TODO: All for exporting different file type (e.g. mp3, wav, etc.)
    processed_filename = f"processed_{base_filename}"
    audio_segment.export(f"testdata/{processed_filename}", format="mp3")

    # Return Filename and Audio Type
    return processed_filename, "audio/mp3"


def parse_query(filename: str, args: Dict) -> Dict:
    return {
        "reverse": False,
        "repeat": 0,
        "slice": {
            "start": 0,
            "end": 0,
        },
    }


def parse_reverse_segment_input(arg: str) -> Dict:
    return {}


def reverse_segment(segment: AudioSegment, inputs: Dict[str, Any]) -> AudioSegment:
    reversed_segment = segment.reverse()

    return reversed_segment


def parse_repeat_segement_input(arg: str) -> Dict:
    multiplier = int(arg)

    return {
        "multiplier": multiplier,
    }


def repeat_segment(segment: AudioSegment, inputs: Dict[str, Any]) -> AudioSegment:
    multiplier = inputs["multiplier"]

    repeated_segment = segment * multiplier
    return repeated_segment


def parse_slice_segement_input(arg: str) -> Dict:
    start_str, end_str = tuple(arg.split(":"))

    start = int(start_str)
    end = int(end_str)

    return {
        "start": start,
        "end": end,
    }


def slice_segment(segment: AudioSegment, inputs: Dict[str, Any]) -> AudioSegment:
    start = inputs["start"]
    end = inputs["end"]

    sliced_segment = segment[start:end]
    return sliced_segment
