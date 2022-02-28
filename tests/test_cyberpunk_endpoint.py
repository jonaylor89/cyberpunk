import pytest

from cyberpunk.cyberpunk_endpoint import CyberpunkEndpoint
from cyberpunk.transformations.reverse import ReverseInput
from cyberpunk.transformations.slice import SliceInput


@pytest.mark.parametrize(
    "key,args,expected",
    [
        ("blah.mp3", {}, CyberpunkEndpoint(audio="blah.mp3")),
        (
            "blah.mp3",
            {"format": "wav"},
            CyberpunkEndpoint(audio="blah.mp3", format="wav"),
        ),
        (
            "blah.mp3",
            {"reverse": "true"},
            CyberpunkEndpoint(
                audio="blah.mp3",
                reverse=ReverseInput(reverse=True),
            ),
        ),
        (
            "blah.mp3",
            {"reverse": "true", "format": "wav"},
            CyberpunkEndpoint(
                audio="blah.mp3",
                reverse=ReverseInput(reverse=True),
                format="wav",
            ),
        ),
        (
            "blah.mp3",
            {"reverse": "true", "slice": "1000:5000", "format": "wav"},
            CyberpunkEndpoint(
                audio="blah.mp3",
                reverse=ReverseInput(reverse=True),
                slice=SliceInput(start=1000, end=5000),
                format="wav",
            ),
        ),
    ],
)
def test_request_parsing(key, args, expected):
    endpoint = CyberpunkEndpoint.from_request(key, args)
    assert endpoint == expected


def test_to_str():
    pass
