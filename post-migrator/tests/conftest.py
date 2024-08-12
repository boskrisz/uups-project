import shutil
import os

import pytest

from app.config import init_config, get_config


# Global Fixtures accessible to all tests
pytest_plugins = [
    "tests.fixtures.asset_manager_service_fixtures",
    "tests.fixtures.database_client_fixtures",
    "tests.fixtures.image_meta_fixtures",
    "tests.fixtures.storage_client_fixtures",
]


@pytest.fixture(scope='function', autouse=True)
def test_setup():
    """ 
    This fixture is used to setup isolated test environments for the tests before running them.
    
    It initializes the test configuration and creates a temporary directory 
    for the generated test assets. This temporary directory is deleted after the test is run.
    """
    test_dir = os.path.join(os.getcwd(), 'test_generated_assets')

    # Remove any leftover directories from previously interrupted tests
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    # Initialize the test configuration
    init_config('test')

    # Make sure that the generated asset directory points to the test directory
    assert get_config().GENERATED_ASSETS_DIR == test_dir

    # Give control to the test
    yield

    # Clean up the test directory
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
