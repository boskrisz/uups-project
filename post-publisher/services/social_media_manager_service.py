import logging

from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError

from clients.social_media_client import SocialMediaClient


class SocialMediaManagerService:
    """
    Service class that manages the posting of images to social media accounts.
    """
    def __init__(self, secret_client: SecretClient) -> None:
        self.secret_client = secret_client
        self.social_media_clients: list[SocialMediaClient] = []


    def add_social_media_account(self, social_media_client: SocialMediaClient) -> None:
        """
        Adds a social media account to the list of registered accounts.

        Args:
            - social_media_client: The social media client object to be registered for posting.
        """
        self.social_media_clients.append(social_media_client)


    def publish_posts(self, image_path: str,
        caption: str) -> None:
        """
        Publishes a post to all registered social media accounts.

        In the case of an exception, the post will be attempted to be published to the next account.

        Args:
            - image_path: The path of the image to be uploaded.
            - caption: The caption for the image.
        """
        for social_media_client in self.social_media_clients:
            try:
                # Retrieve the credentials for the social media account
                account_id = self.secret_client \
                    .get_secret(social_media_client.name + "-account-id").value
                access_token = self.secret_client \
                    .get_secret(social_media_client.name + "-access-token").value
            except ResourceNotFoundError:
                logging.error("Failed to get credentials for %s.", social_media_client.name)
                continue

            try:
                # Publish the post to the social media account
                social_media_client.publish_post(
                    image_path=image_path,
                    caption=caption,
                    account_id=account_id,
                    access_token=access_token
                )
            except Exception:
                # Error is logged already, continue with the next account
                continue
