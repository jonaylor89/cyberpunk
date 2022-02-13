
from pydub import AudioSegment
from typing import Dict, Tuple


def process_args(base_filename: str, args: Dict) -> Tuple[str, str]:

    lookup_table = {
        "reverse": reverse_segment,
        "repeat": repeat_segment,
        "slice": slice_segment,
    }

    # Create Audio Segment
    audio_segment = AudioSegment.from_mp3(f"testdata/{base_filename}")

    # Pass Audio Segment through Each Stage
    for (k, v) in args.items():
        print(f"{k} = {v}")

        if k in lookup_table.keys(): 
            audio_segment = lookup_table[k](audio_segment, v)

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


def reverse_segment(segment: AudioSegment, args: str) -> AudioSegment:
    return segment

def repeat_segment(args: str) -> AudioSegment:
    return segment

def slice_segment(segment: AudioSegment, args: str) -> AudioSegment:
    return segment