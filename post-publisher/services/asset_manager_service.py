import logging
from typing import Union

from config import get_config
from clients.storage_client import StorageClient
from clients.database_client import DatabaseClient
from exceptions.database_client_exceptions import (
    DatabaseSelectQueryException,
    DatabaseUpdateQueryException
)


class AssetManagerService:
    """
    Service class that manages the generated images and their metadata.
    """
    def __init__(self, storage_client: StorageClient,
        database_client: DatabaseClient) -> None:
        self.storage_client = storage_client
        self.database_client = database_client


    def get_approved_image_meta(self) -> Union[dict, None]:
        """
        Retrieves the metadata of an approved image from the Cosmos DB.
        """
        try:
            return self.database_client.find_one_by_published(published=False)
        except DatabaseSelectQueryException as e:
            logging.error("%s failed to retrieve approved image metadata.",
                e.cloud_database_name, exc_info=True)
            raise e


    def get_image_path(self, image_meta: dict) -> str:
        """
        Retrieve the path of the image from the blob storage.

        Args:
            - image_meta: The metadata of the image to retrieve.
        """
        img_name = image_meta['id'] + '.jpg'

        # Get an access token to be able to read the image from the storage account
        sas_token = self.storage_client.get_access_token(img_name)

        # Construct the URL of the image with the access token
        img_url = get_config().STORAGE_ACCOUNT_URL + get_config().STORAGE_CONTAINER_NAME \
            + '/' + img_name + '?' + sas_token

        return img_url


    def update_published_status(self, image_meta: dict) -> None:
        """
        Update the published status of an image in the database.

        Args:
            - image_meta: The metadata of the image to update.
        """
        try:
            self.database_client.update_published_status(
                document_id=image_meta['id'],
                published=True
            )
        except DatabaseUpdateQueryException as e:
            logging.error("%s failed to update image metadata in database",
                e.cloud_database_name, exc_info=True)
            raise e
