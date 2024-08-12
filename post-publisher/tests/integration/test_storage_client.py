from datetime import datetime, timedelta
from urllib.parse import unquote
from urllib.request import urlretrieve

from config import get_config
from clients.storage_client import AzureStorageClient


def test_get_access_token_enables_short_lived_read_access_to_blob(
    test_storage_account_client: AzureStorageClient,
    dummy_img_in_blob_storage: str
    ):
    """
    GIVEN a test StorageClient instance
        AND a dummy file uploaded to the test container
    WHEN the get_access_token method is called with a file name
    THEN it should return a short-lived read-only access token for the given file.
    """
    # Get an access token for the dummy file
    access_token = test_storage_account_client.get_access_token(dummy_img_in_blob_storage)
    params = dict(param.split('=') for param in access_token.split('&'))

    # Assert that the access token is read-only
    assert params.get('sp') == 'r'

    # Assert that the access token is valid for 5 minutes
    start_time = datetime.strptime(unquote(params['st']), "%Y-%m-%dT%H:%M:%SZ")
    end_time = datetime.strptime(unquote(params['se']), "%Y-%m-%dT%H:%M:%SZ")
    assert end_time - start_time == timedelta(minutes=5)

    # Assert that the access token can be used to read the file
    url = get_config().STORAGE_ACCOUNT_URL \
        + get_config().STORAGE_CONTAINER_NAME \
        + '/' + dummy_img_in_blob_storage \
        + '?' + access_token

    try:
        urlretrieve(url, dummy_img_in_blob_storage)
    except Exception as e:
        assert False, f"Failed to download file with access token: {e}"
