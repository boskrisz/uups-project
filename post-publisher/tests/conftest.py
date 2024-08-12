import os
import pytest

from config import init_config


# Global Fixtures accessible to all tests
pytest_plugins = [
    "tests.fixtures.asset_fixtures",
    "tests.fixtures.asset_manager_service_fixtures",
    "tests.fixtures.authentication_fixtures",
    "tests.fixtures.database_client_fixtures",
    "tests.fixtures.secret_client_fixtures",
    "tests.fixtures.social_media_client_fixtures",
    "tests.fixtures.storage_client_fixtures",
]


@pytest.fixture(scope='session', autouse=True)
def test_setup():
    """ 
    This fixture is used to setup isolated test environments for the tests before running them.
    It initializes the test configuration.
    """
    # Initialize the test configuration
    os.environ['UUPS_ENV'] = 'test'
    init_config(os.environ['UUPS_ENV'])

    # Give control to the test
    yield
