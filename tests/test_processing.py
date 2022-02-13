import pytest

from cyberpunk.processing import process_args, parse_query


def test_process_args():
    output = process_args("blah.mp3", {"reverse": "true"})

    assert output == ("blah.mp3", "audio/mp3")
