from config import get_config
from services.asset_manager_service import AssetManagerService


def test_get_image_path_correctly_assembles_url(
    mock_asset_manager_service: AssetManagerService
    ):
    """
    GIVEN a mocked AssetManagerService instance
        AND a dummy image metadata
    WHEN the image path is retrieved for the image metadata
    THEN it should return its correct URL
    """
    # Initialize dummy image metadata
    image_meta = {
        'id': 'test_image'
    }

    # Call the image url path retrieval method
    img_url = mock_asset_manager_service.get_image_path(image_meta)

    # Assert the correct URL is returned
    assert img_url == get_config().STORAGE_ACCOUNT_URL \
        + get_config().STORAGE_CONTAINER_NAME + '/' \
        + image_meta['id'] + '.jpg' \
        + '?TESTSASTOKEN'
