import logging
from abc import ABC, abstractmethod

import requests

from exceptions.social_media_client_exceptions import (
    InstagramMediaUploadException,
    InstagramMediaPublishException
)


class SocialMediaClient(ABC):
    """
    Abstract class for a social media client.
    """
    @abstractmethod
    def publish_post(self,
        image_path: str,
        caption: str,
        account_id: str,
        access_token: str) -> None:
        """
        Publishes a post to the social media platform.
        """
        pass


class InstagramClient(SocialMediaClient):
    """
    A client class for interacting with Instagram.
    """
    def __init__(self) -> None:
        self.name="instagram"
        self.api_version = "v20.0"
        self.base_url = "https://graph.facebook.com/" + self.api_version + "/"


    def upload_image_to_container(self,
        caption: str,
        image_url: str,
        account_id: str,
        access_token: str):
        """
        Uploads an image to a media container in Instagram.

        Args:
            - caption: The caption for the image.
            - image_url: The URL of the image to be uploaded.
            - account_id: The ID of the Instagram account where the post will be published.
            - access_token: The access token for the Instagram account.

        Returns:
            The ID of the container that stores the uploaded image.
        """
        # Define the URL for creating a media contrainer
        url = self.base_url + account_id + '/media'

        # Define the parameters for the request
        param = {
            'access_token': access_token,
            'caption': caption,
            'image_url': image_url
        }

        # Send the request to the Instagram API
        response = requests.post(url, params=param, timeout=60)
        response = response.json()

        if response.get('error'):
            logging.error("Failed to upload image to Instagram's media container.", exc_info=True)
            raise InstagramMediaUploadException(error_code=response['error']['code'],
                error_message=response['error']['message'])

        container_id = response['id']
        return container_id


    def publish_post(self, image_path: str,
        caption: str,
        account_id: str,
        access_token: str) -> None:
        """
        Uploads an image post with a caption to Instagram.

        Args:
            - image_path: The path of the image to be uploaded.
            - caption: The caption for the image.
            - account_id: The ID of the Instagram account where the post will be published.
            - access_token: The access token for the Instagram account.
        """
        logging.info("Uploading post to Instagram...")

        # Define the URL for publishing the image
        url = self.base_url + account_id + '/media_publish'

        # Upload the image to Instagram's media container
        container_id = self.upload_image_to_container(
            caption=caption,
            image_url=image_path,
            account_id=account_id,
            access_token=access_token
        )

        # Define the parameters for the request
        param = {
            'access_token': access_token,
            'creation_id': container_id
        }

        # Publish the post to Instagram
        response = requests.post(url, params=param, timeout=60)
        response = response.json()

        if response.get('error'):
            logging.error("Failed to publish post to Instagram.", exc_info=True)
            raise InstagramMediaPublishException(error_code=response['error']['code'],
                error_message=response['error']['message'])

        logging.info("Post with ID '%s' uploaded to Instagram successfully.", response['id'])
