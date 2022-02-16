import os
import tempfile
import pytest

from cyberpunk.server import create_app


@pytest.fixture
def client():
    # db_fd, db_path = tempfile.mkstemp()
    app = create_app()

    with app.test_client() as client:
        # with app.app_context():
        #     init_db()
        yield client

    # os.close(db_fd)
    # os.unlink(db_path)


def test_root(client):
    """Start with an empty route."""

    rv = client.get("/")
    assert rv.data == b"Hello World"
