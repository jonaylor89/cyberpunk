from functools import wraps
from typing import Dict, Tuple
from uuid import UUID

_processed_audio_cache: Dict[Tuple, Tuple] = {}


def cached_result(func):
    @wraps(func)
    def wrapper(request_id: UUID, key: str, args: Dict):
        if (key, args) in _processed_audio_cache.keys():
            return _processed_audio_cache[(key, args)]

        result = func(request_id, key, args)
        _processed_audio_cache[(key, args)] = result
        return result

    return wrapper
