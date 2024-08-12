import os

from PIL import Image

from app.config import get_config
from app.clients.storage_client import AzureStorageClient


def test_upload_file(test_storage_account_client: AzureStorageClient):
    """
    GIVEN a test Azure Storage Client instance
    WHEN its upload file method is called with a dummy file
    THEN it should upload the file to the specified container.
    """
    # Create a dummy image
    image_name = 'test_image.jpg'
    image = Image.new('RGB', (10, 10))

    # Save the image as JPG
    image_path = os.path.join(get_config().APPROVED_IMAGE_DIR, image_name)
    image.save(image_path)

    # Upload the image to the Azure Blob Storage
    test_storage_account_client.upload_file(image_path, image_name)

    # Check that the image was uploaded successfully
    blob_client = test_storage_account_client.container_client.get_blob_client(image_name)
    assert blob_client.exists()
