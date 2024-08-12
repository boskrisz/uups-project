from typing import Generator

from unittest.mock import patch
import pytest
from azure.identity import DefaultAzureCredential

from config import get_config
from clients.storage_client import AzureStorageClient


@pytest.fixture
def mock_storage_account_client() -> Generator[AzureStorageClient, None, None]:
    """
    Mock the Azure Storage Account client instance.
    """
    with patch.object(AzureStorageClient, '_init_blob_service_client', return_value=None), \
        patch.object(AzureStorageClient, '_request_user_delegation_key', return_value=None), \
        patch.object(AzureStorageClient, 'get_access_token', return_value="TESTSASTOKEN"):
        mock_instance = AzureStorageClient(
            account_url=get_config().STORAGE_ACCOUNT_URL,
            container_name=get_config().STORAGE_CONTAINER_NAME,
            credential=None
        )
        yield mock_instance


@pytest.fixture
def test_storage_account_client(
    azure_managed_identity: DefaultAzureCredential
    ) -> Generator[AzureStorageClient, None, None]:
    """
    Create an Azure Storage Account client instance for testing.
    This fixture also cleans up the test storage container after the test is run.
    """
    assert "test" in get_config().STORAGE_ACCOUNT_URL, \
        "Test environment must be used for this fixture"

    test_client = AzureStorageClient(
        account_url=get_config().STORAGE_ACCOUNT_URL,
        container_name=get_config().STORAGE_CONTAINER_NAME,
        credential=azure_managed_identity
    )

    # Clean up previously stuck blobs in the container, if there's any
    test_client.delete_all_blobs_in_container()

    yield test_client

    # Clean up the test storage account
    test_client.delete_all_blobs_in_container()
