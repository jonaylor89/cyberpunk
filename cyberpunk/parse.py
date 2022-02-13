from typing import Dict


def parse_query(query: str, args: Dict) -> Dict:
    return {
        "reverse": False,
        "repeat": 0,
        "slice_start": 0,
        "slice_end": 0,
    }
