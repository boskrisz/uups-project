from clients.social_media_client import InstagramClient
from services.social_media_manager_service import SocialMediaManagerService


def test_publish_post_publishes_to_all_accounts(
    mock_key_vault_client,
    mock_instagram_clients: list[InstagramClient]
    ):
    """
    GIVEN multiple mocked social media accounts
        AND a mocked key vault that stores dummy access tokens for these accounts
        AND a social media manager service that manages these accounts
    WHEN the service is called to publish a post
    THEN the post should be published to all accounts
    """
    # Initialize the social media manager service
    social_media_manager_service = SocialMediaManagerService(mock_key_vault_client)

    # Add the mocked Instagram clients to the service
    for client in mock_instagram_clients:
        social_media_manager_service.add_social_media_account(client)

    # Publish the post to all registered social media accounts
    social_media_manager_service.publish_posts("test.jpg", "Test caption")

    # Assert that the post was published to all accounts
    for client in mock_instagram_clients:
        client.publish_post.assert_called_once_with(
            image_path="test.jpg",
            caption="Test caption",
            account_id=mock_key_vault_client.get_secret("instagram-account-id").value,
            access_token=mock_key_vault_client.get_secret("instagram-access-token").value
        )
