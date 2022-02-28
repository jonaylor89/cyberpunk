import pytest
from pydub import AudioSegment

from cyberpunk.transformations.reverse import Reverse, ReverseInput


@pytest.mark.parametrize(
    "arg,expected",
    [
        ("True", ReverseInput(reverse=True)),
        ("true", ReverseInput(reverse=True)),
        ("Y", ReverseInput(reverse=True)),
        ("y", ReverseInput(reverse=True)),
        ("yes", ReverseInput(reverse=True)),
        ("1", ReverseInput(reverse=True)),
        ("0", ReverseInput(reverse=False)),
        ("blah", ReverseInput(reverse=False)),
        ("no", ReverseInput(reverse=False)),
        ("no", ReverseInput(reverse=False)),
        ("false", ReverseInput(reverse=False)),
        ("False", ReverseInput(reverse=False)),
    ],
)
def test_reverse_parsing(arg, expected):
    output = ReverseInput.from_str(arg)
    assert output == expected


@pytest.mark.parametrize(
    "arg",
    [ReverseInput(reverse=True), ReverseInput(reverse=False)],
)
def test_reverse_processing(arg):
    segment = AudioSegment.from_file("testdata/celtic_pt2.mp3")
    output = Reverse().run(segment, arg)
    assert output != AudioSegment.empty()
