from typing import Generator

from unittest.mock import patch
import pytest

from clients.social_media_client import InstagramClient


@pytest.fixture
def mock_instagram_client() -> Generator[InstagramClient, None, None]:
    """
    Mock the Instagram Graph API client instance.
    """
    with patch.object(InstagramClient, 'upload_image_to_container', return_value='0001'), \
        patch.object(InstagramClient, 'publish_post', return_value=None):
        mock_instance = InstagramClient()
        yield mock_instance


@pytest.fixture
def mock_instagram_clients() -> Generator[list[InstagramClient], None, None]:
    """
    Mock multiple Instagram Graph API client instances.
    """
    mock_instance_1 = InstagramClient()
    mock_instance_2 = InstagramClient()

    # Mock the methods separately for each instance,
    # so they can be tested individually
    with patch.object(mock_instance_1, 'upload_image_to_container', return_value='0001'), \
        patch.object(mock_instance_1, 'publish_post', return_value=None), \
        patch.object(mock_instance_2, 'upload_image_to_container', return_value='0002'), \
        patch.object(mock_instance_2, 'publish_post', return_value=None):
        yield [mock_instance_1, mock_instance_2]
