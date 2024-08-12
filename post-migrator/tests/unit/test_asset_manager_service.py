import os

from unittest.mock import call

from app.config import get_config
from app.services.asset_manager_service import AssetManagerService


def test_upload_images_called_with_proper_params(mock_asset_manager_service: AssetManagerService):
    """
    GIVEN a mocked AssetManagerService instance
    WHEN the images are uploaded to the storage account
    THEN the storage account's file upload method should be called with the proper parameters
    """
    # Initialize some dummy image paths
    dummy_images = ['image1.jpg', 'image2.jpg', 'image3.jpg']
    dummy_image_paths = [os.path.join(get_config().APPROVED_IMAGE_DIR, img) for img in dummy_images]

    # Call the upload images method
    mock_asset_manager_service.upload_images(dummy_image_paths)

    # Check that the upload images method was called with the proper parameters
    expected_calls = [
        call(file_path=img_path, file_name=os.path.basename(img_path))
        for img_path in dummy_image_paths
    ]
    mock_asset_manager_service.storage_client.upload_file.assert_has_calls(expected_calls)
