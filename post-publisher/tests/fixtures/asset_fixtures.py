import os
from typing import Generator

from PIL import Image
from azure.storage.blob import ContentSettings

import pytest

from clients.database_client import CosmosDbClient
from clients.storage_client import AzureStorageClient


@pytest.fixture
def dummy_img_in_blob_storage(
    test_storage_account_client: AzureStorageClient
    ) -> Generator[str, None, None]:
    """
    Upload a dummy image to the test blob storage container.
    """
    # Create a dummy image
    image_name = '123.jpg'
    image = Image.new('RGB', (10, 10))

    # Upload the dummy image to the test container
    test_storage_account_client.container_client.upload_blob(
        name=image_name,
        data=image.tobytes(),
        content_settings=ContentSettings(
            content_type="image/jpg"
        ))

    yield image_name

    # Clean up the test image
    test_storage_account_client.container_client.delete_blob(image_name)
    if os.path.exists(image_name):
        os.remove(image_name)


@pytest.fixture
def dummy_img_meta_in_db(
    test_cosmosdb_client: CosmosDbClient
    ) -> Generator[str, None, None]:
    """
    Insert a dummy image metadata document to the test Cosmos DB container.
    """
    # Create a dummy metadata document
    image_meta = {
        "id": "123", # same as image name
        "caption": "test caption",
        "published": False
    }

    # Insert the dummy metadata document to the test container
    test_cosmosdb_client.container_client.create_item(body=image_meta)

    yield image_meta

    # Clean up the test metadata document
    test_cosmosdb_client.container_client.delete_item(
        item=image_meta['id'],
        partition_key=image_meta['id']
    )
