import pytest
from pydub import AudioSegment

from cyberpunk.transformations import Reverse


@pytest.mark.parametrize(
    "arg,expected",
    [
        ("True", {"reverse": True}),
        ("true", {"reverse": True}),
        ("Y", {"reverse": True}),
        ("y", {"reverse": True}),
        ("yes", {"reverse": True}),
        ("1", {"reverse": True}),
        ("0", {"reverse": False}),
        ("blah", {"reverse": False}),
        ("no", {"reverse": False}),
        ("false", {"reverse": False}),
        ("False", {"reverse": False}),
    ],
)
def test_reverse_parsing(arg, expected):
    output = Reverse().parse_input_from_str(arg)
    assert output == expected


@pytest.mark.parametrize("arg", [{"reverse": True}, {"reverse": False}])
def test_reverse_processing(arg):
    segment = AudioSegment.from_file("testdata/celtic_pt2.mp3")
    output = Reverse().process(segment, arg)
    assert output != AudioSegment.empty()
