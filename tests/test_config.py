import pytest

from cyberpunk.config import CyberpunkConfig


@pytest.fixture
def default_config():
    # db_fd, db_path = tempfile.mkstemp()
    config = CyberpunkConfig()

    yield config


def test_defaults(default_config):
    audio_store = default_config.audio_store

    assert audio_store == "local"
