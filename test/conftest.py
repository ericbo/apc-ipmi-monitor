import os
import pathlib

import pytest


@pytest.fixture(scope="session")
def root_path():
    test_dir_path = pathlib.Path(__file__).parent.absolute()

    return os.path.join(test_dir_path, "..")
