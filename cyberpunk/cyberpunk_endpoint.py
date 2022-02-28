import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type

from cyberpunk.transformations import TransformationInput
from cyberpunk.transformations.concat import ConcatInput
from cyberpunk.transformations.fade_in import FadeInInput
from cyberpunk.transformations.fade_out import FadeOutInput
from cyberpunk.transformations.repeat import RepeatInput
from cyberpunk.transformations.reverse import ReverseInput
from cyberpunk.transformations.slice import SliceInput


@dataclass
class CyberpunkEndpoint:
    """
    {
        "audio": "celtic_pt2.mp3",
        "hash": "=",
        "reverse": true,
        "repeat": 1,
        "slice": {
            "start": 1000,
            "end": 5000,
        }
    }
    """

    # path: str
    audio: str
    hash: str = "unsafe"
    format: str = "mp3"
    reverse: Optional[ReverseInput] = None
    repeat: Optional[RepeatInput] = None
    slice: Optional[SliceInput] = None
    fade_in: Optional[FadeInInput] = None
    fade_out: Optional[FadeOutInput] = None
    concat: Optional[ConcatInput] = None

    @classmethod
    def from_request(cls, key: str, args: Dict):
        endpoint = cls(audio=key, hash="unsafe")

        lookup_table: Dict[str, Type[TransformationInput]] = {
            "reverse": ReverseInput,
            "repeat": RepeatInput,
            "slice": SliceInput,
            "concat": ConcatInput,
            "fade_in": FadeInInput,
            "fade_out": FadeOutInput,
        }

        supported_formats: List[str] = [
            "mp3",
            "wav",
            "flac",
        ]

        # Parse request args and fill corresponding fields
        for (k, v) in args.items():
            if k in lookup_table.keys():

                logging.info(f"parsing transformation input: {k}")
                parser: Type[TransformationInput] = lookup_table[k]

                try:
                    inputs: Dict[str, Any] = parser.from_str(v)
                except Exception as e:
                    logging.error(
                        f"failure to parse input `{v}` for `{k}` : {e}",
                    )
                    continue

                # This only works because attributes are the same name
                # as the query parameters. If that stops being the case,
                # another map/lookup-table will need to be used
                # i.e. setattr(endpoint, param_to_attr[k], inputs)
                setattr(endpoint, k, inputs)

        # default formatting is mp3
        file_format = (
            args["format"]
            if "format" in args.keys() and args["format"] in supported_formats
            else "mp3"
        )

        endpoint.format = file_format

        return endpoint

    def __repr__(self) -> str:
        params = []

        if self.reverse is not None:
            params.append(f"reverse={self.reverse}")
        if self.repeat is not None:
            params.append(f"repeat={self.repeat}")
        if self.slice is not None:
            params.append(f"slice={self.slice}")
        if self.concat is not None:
            params.append(f"concat={self.concat}")
        if self.fade_in is not None:
            params.append(f"fade_in={self.fade_in}")
        if self.fade_out is not None:
            params.append(f"fade_out={self.fade_out}")

        return f"/{self.audio}{('?' + '&'.join(params)) if len(params) > 0 else ''}"

    def __str__(self) -> str:
        params = []

        if self.reverse is not None:
            params.append(f"reverse={self.reverse}")
        if self.repeat is not None:
            params.append(f"repeat={self.repeat}")
        if self.slice is not None:
            params.append(f"slice={self.slice}")
        if self.concat is not None:
            params.append(f"concat={self.concat}")
        if self.fade_in is not None:
            params.append(f"fade_in={self.fade_in}")
        if self.fade_out is not None:
            params.append(f"fade_out={self.fade_out}")

        return f"/{self.audio}{('?' + '&'.join(params)) if len(params) > 0 else ''}"
