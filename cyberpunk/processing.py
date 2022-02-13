from typing import Dict, Tuple


def process_args(base_filename: str, args: Dict) -> Tuple[str, str]:
    print(args)

    return base_filename, "audio/mp3"

def parse_query(filename: str, args: Dict) -> Dict:
    return {
        "reverse": False,
        "repeat": 0,
        "slice_start": 0,
        "slice_end": 0,
    }
