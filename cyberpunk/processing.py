import logging
from typing import Any, Dict, List, Tuple

from cyberpunk.storage import get_storage
from cyberpunk.transformations import (
    Concat,
    FadeIn,
    FadeOut,
    Repeat,
    Reverse,
    Slice,
    Transformation,
)


def process_args(base_filename: str, args: Dict) -> Tuple[str, str]:

    lookup_table: Dict[str, Transformation] = {
        "reverse": Reverse(),
        "repeat": Repeat(),
        "slice": Slice(),
        "concat": Concat(),
        "fade_in": FadeIn(),
        "fade_out": FadeOut(),
    }

    supported_formats: List[str] = [
        "mp3",
        "wav",
        "flac",
    ]

    # Create Audio Segment
    audio_segment, tmp_location = get_storage().get_segment(base_filename)

    # Pass Audio Segment through Each Stage
    for (k, v) in args.items():
        if k in lookup_table.keys():

            logging.info(f"running transformation: {k}")

            transformation: Transformation = lookup_table[k]
            assert transformation is not None

            try:
                inputs: Dict[str, Any] = transformation.parse_input_from_str(v)
            except Exception as e:
                logging.error(f"failure to parse input `{v}` for `{k}` : {e}")
                continue

            try:
                audio_segment = transformation.process(audio_segment, inputs)
            except Exception as e:
                logging.error(
                    f"failure to process input `{v}` for `{k}` : {e}",
                )
                continue

    # TODO this can be significantly better
    file_format = "mp3"
    if "format" in args.keys():
        file_format = (
            args["format"] if args["format"] in supported_formats else "mp3"
        )

    processed_filename = get_storage().save_segment(
        tmp_location,
        audio_segment,
        file_format,
    )

    # Return Filename and Audio Type
    return processed_filename, f"audio/{file_format}"


def parse_query(filename: str, args: Dict) -> Dict:
    """
    Parse and generate a Python object based on a cyberpunk endpoint
    """
    return {"audio": filename, **args}


def cyberpunk_path():
    """
    Parse and generate a cyberpunk endpoint based on a Python object
    """
    return
