import pytest

from cyberpunk.storage import LocalStorage

@pytest.fixture
def local_storage():
    storage = LocalStorage() 

    yield storage

def test_local(local_storage):
    base_dir = local_storage.base_dir 

    assert base_dir == 'testdata/'