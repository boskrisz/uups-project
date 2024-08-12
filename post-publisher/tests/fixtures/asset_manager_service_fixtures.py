import pytest

from clients.database_client import CosmosDbClient
from clients.storage_client import AzureStorageClient
from services.asset_manager_service import AssetManagerService


@pytest.fixture
def mock_asset_manager_service(mock_cosmosdb_client: CosmosDbClient,
    mock_storage_account_client: AzureStorageClient) -> AssetManagerService:
    """
    Creates a default AssetManagerService instance with mocked clients.
    """
    return AssetManagerService(
        storage_client=mock_storage_account_client,
        database_client=mock_cosmosdb_client
    )
