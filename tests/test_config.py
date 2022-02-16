import pytest

from cyberpunk.config import CyberpunkConfig


@pytest.fixture
def default_config():
    # db_fd, db_path = tempfile.mkstemp()
    config = CyberpunkConfig()

    yield config


def test_defaults(default_config):
    port = default_config.port

    assert port == 5000
