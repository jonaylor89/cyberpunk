from typing import Dict


def parse_url(query: str) -> Dict:
    return {
        "reverse": False,
        "repeat": 0,
        "slice_start": 0,
        "slice_end": 0,
    }
