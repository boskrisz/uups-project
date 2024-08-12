from typing import Generator

from unittest.mock import patch
import pytest
from azure.identity import DefaultAzureCredential

from config import get_config
from clients.database_client import CosmosDbClient


@pytest.fixture
def mock_cosmosdb_client() -> Generator[CosmosDbClient, None, None]:
    """
    Mock the Azure Cosmos DB client instance.
    """
    with patch.object(CosmosDbClient, '_init_database_client', return_value=None), \
        patch.object(CosmosDbClient, 'init_container_client', return_value=None), \
        patch.object(CosmosDbClient, 'find_one_by_published', return_value={
            "id": "123",
            "published": False
        }), \
        patch.object(CosmosDbClient, 'update_published_status', return_value=None):
        mock_instance = CosmosDbClient(
            account_url=get_config().COSMOSDB_ACCOUNT_URL,
            database_name=get_config().COSMOSDB_DATABASE_NAME,
            container_name=get_config().COSMOSDB_CONTAINER_NAME,
            credential=None
        )
        yield mock_instance


@pytest.fixture
def test_cosmosdb_client(
    azure_managed_identity: DefaultAzureCredential
    ) -> Generator[CosmosDbClient, None, None]:
    """
    Create a Cosmos DB client instance for testing.
    This fixture also cleans up the test database after the test is run.
    """
    assert "test" in get_config().COSMOSDB_ACCOUNT_URL, \
        "Test environment must be used for this fixture"

    test_client = CosmosDbClient(
        account_url=get_config().COSMOSDB_ACCOUNT_URL,
        database_name=get_config().COSMOSDB_DATABASE_NAME,
        container_name=get_config().COSMOSDB_CONTAINER_NAME,
        credential=azure_managed_identity
    )

    # Clean up previously stuck items in the container, if there's any
    test_client.delete_all_items_from_container()

    yield test_client

    # Clean up the test database
    test_client.delete_all_items_from_container()
