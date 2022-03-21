import logging
from dataclasses import asdict
from typing import Dict, Tuple
from uuid import UUID

from cyberpunk.cache import cached_result
from cyberpunk.cyberpunk_endpoint import CyberpunkEndpoint
from cyberpunk.storage import get_storage
from cyberpunk.transformations import Transformation
from cyberpunk.transformations.concat import Concat
from cyberpunk.transformations.fade_in import FadeIn
from cyberpunk.transformations.fade_out import FadeOut
from cyberpunk.transformations.repeat import Repeat
from cyberpunk.transformations.reverse import Reverse
from cyberpunk.transformations.slice import Slice


@cached_result
def process_args(request_id: UUID, key: str, args: Dict) -> Tuple[str, str]:
    """
    @param request_id: the id for the http request performing the process
    @param key: key to the audiofile (i.e. filename/id)
    @param args: the transformations and manipulations to be done on `key`
    @return a tuple contains the new processed audio key and the content type
    """

    endpoint = CyberpunkEndpoint.from_req(key, args)

    instruction_lookup: Dict[str, Transformation] = {
        "reverse": Reverse(),
        "repeat": Repeat(),
        "slice": Slice(),
        "concat": Concat(),
        "fade_in": FadeIn(),
        "fade_out": FadeOut(),
    }

    # Create Audio Segment
    audio_segment, tmp_location = get_storage().get_segment(key)

    # Pass Audio Segment through Each Stage
    for (k, v) in args.items():
        if k in instruction_lookup.keys():

            logging.info(f"running transformation: {k}")

            transformation: Transformation = instruction_lookup[k]
            assert transformation is not None

            try:

                # This only works because attributes are the same name
                # as the query parameters. If that stops being the case,
                # another map/lookup-table will need to be used
                # i.e. getattr(endpoint, param_to_instruction[k])
                inputs = getattr(endpoint, k)

                audio_segment = transformation.run(audio_segment, inputs)
            except Exception as e:
                logging.error(
                    f"failure to process input `{v}` for `{k}` : {e}",
                )
                continue

    processed_filename = get_storage().save_segment(
        request_id,
        audio_segment,
        endpoint.format,
    )

    # Return Filename and Audio Type
    return processed_filename, f"audio/{endpoint.format}"


def parse_query(key: str, args: Dict) -> Dict:
    """
    Parse and generate a Python object based on a cyberpunk endpoint
    @param key: key to the audiofile (i.e. filename/id)
    @param args: the transformations and manipulations to be done on `key`
    @return: the serialized cyberpunk endpoint object
    """

    endpoint = CyberpunkEndpoint.from_req(key, args)
    return asdict(endpoint)


def cyberpunk_path(endpoint: CyberpunkEndpoint) -> str:
    """
    Parse and generate a cyberpunk endpoint based on a Python object
    @param endpoint: a cyberpunk endpoint object
    @return: the endpoint deserialized as a string
    """

    return str(endpoint)
