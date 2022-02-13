import os
import tempfile
import pytest

from cyberpunk.main import app


@pytest.fixture
def client():
    # db_fd, db_path = tempfile.mkstemp()
    # app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        # with app.app_context():
        #     init_db()
        yield client

    # os.close(db_fd)
    # os.unlink(db_path)

def test_root(client):
    """Start with an empty route."""

    rv = client.get('/')
    assert b'Hello World' == rv.data