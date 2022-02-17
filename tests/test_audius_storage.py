import pytest
from pydub import AudioSegment

from cyberpunk.storage import AudiusStorage


@pytest.fixture
def audius_storage():
    storage = AudiusStorage()

    yield storage


def test_get_segment(audius_storage):
    segment = audius_storage.get_segment("7YmNr")

    assert segment != AudioSegment.empty()
