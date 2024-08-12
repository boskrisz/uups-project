from typing import Generator

from unittest.mock import patch
import pytest

from app.config import get_config
from app.clients.storage_client import AzureStorageClient


@pytest.fixture
def mock_storage_account_client() -> Generator[AzureStorageClient, None, None]:
    """
    Mock the Azure Storage Account client instance.
    """
    with patch.object(AzureStorageClient, '_init_container_client', return_value=None), \
        patch.object(AzureStorageClient, 'upload_file', return_value=None):
        mock_instance = AzureStorageClient(
            account_url=get_config().STORAGE_ACCOUNT_URL,
            container_name=get_config().STORAGE_CONTAINER_NAME,
            sas_token=get_config().STORAGE_CONTAINER_SAS
        )
        yield mock_instance


@pytest.fixture
def test_storage_account_client() -> Generator[AzureStorageClient, None, None]:
    """
    Create an Azure Storage Account instance for testing.
    This fixture also cleans up the test storage account after the test is run.
    """
    assert "test" in get_config().STORAGE_ACCOUNT_URL, \
        "Test environment must be used for this fixture"

    test_client = AzureStorageClient(
        account_url=get_config().STORAGE_ACCOUNT_URL,
        container_name=get_config().STORAGE_CONTAINER_NAME,
        sas_token=get_config().STORAGE_CONTAINER_SAS
    )

    # Clean up previously stuck blobs in the container, if there's any
    test_client.delete_all_blobs_in_container()

    yield test_client

    # Clean up the test storage account
    test_client.delete_all_blobs_in_container()
