import csv
import os
import shutil
from glob import glob
from typing import Tuple

from app.config import get_config
from app.config.log_config import logger
from app.models.image_meta import ImageMeta
from app.clients.database_client import DatabaseClient
from app.clients.storage_client import StorageClient


class AssetManagerService:
    """
    Service class for managing the generated images and their metadata.

    Attributes:
        - storage_client: The client for the cloud storage account.
        - database_client: The client for the cloud database.
    """
    def __init__(self, storage_client: StorageClient,
        database_client: DatabaseClient) -> None:
        self.storage_client: StorageClient = storage_client
        self.database_client: DatabaseClient = database_client


    def get_approved_assets(self) -> Tuple[list[str], list[ImageMeta]]:
        """
        Get the approved images and their metadata.
        """
        img_paths = self.get_approved_image_paths()

        if not img_paths:
            return [], []

        img_metas = self.get_approved_image_metas(img_paths)
        return img_paths, img_metas


    @staticmethod
    def get_approved_image_paths() -> list[str]:
        """
        Get the paths of all generated images that have been approved.
        """
        return glob(get_config().APPROVED_IMAGE_DIR + "/" + '*.jpg')


    @staticmethod
    def get_approved_image_metas(image_paths: list[str]) -> list[ImageMeta]:
        """
        Get the metadata of the approved images.

        Args:
            - image_paths: The paths of the images to get the metadata for.
        """
        # Get the ids of the images
        image_ids = [os.path.basename(image_path).split('.')[0] for image_path in image_paths]

        # Find the approved images' metadata
        approved_image_metas = []
        try:
            with open(get_config().IMAGE_META_FILE, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=',')

                for row in reader:
                    if row['id'] in image_ids:
                        approved_image_metas.append(ImageMeta(**row))
        except Exception as e:
            logger.error("Failed to read image metadata from '%s'.",
                get_config().IMAGE_META_FILE, exc_info=True)
            raise e

        return approved_image_metas


    def upload_images(self, image_paths: list[str]) -> None:
        """
        Upload the images to the configured storage account.

        Args:
            - image_paths: The paths of the images to be uploaded.
        """
        for image_path in image_paths:
            self.storage_client.upload_file(
                file_path=image_path,
                file_name=os.path.basename(image_path)
            )

        logger.info("Images uploaded to the '%s' container in the '%s' storage account.",
            get_config().STORAGE_CONTAINER_NAME, get_config().STORAGE_ACCOUNT_URL)


    def upload_image_metas(self, img_metas: list[ImageMeta]) -> None:
        """
        Upload the metadata of the images to the configured database.

        Args:
            - img_metas: The metadata of the images to be uploaded.
        """
        for img_meta in img_metas:
            # Add published flag to the image metadata
            # indicating that the image has not been published to social media
            img_meta = img_meta.to_json()
            img_meta['published'] = False

            # Insert the image metadata into the database
            self.database_client.insert_record(img_meta)

        logger.info("Image metadata uploaded to the '%s' container in the '%s' database.",
            get_config().COSMOSDB_CONTAINER_NAME, get_config().COSMOSDB_DATABASE_NAME)


    @staticmethod
    def move_images_to_processed(image_paths: list[str]) -> None:
        """
        Move the processed images from the approved folder to the processed folder.

        Args:
            - image_paths: The path of the image to be moved to the processed folder.
        """
        for image_path in image_paths:
            file_name = os.path.basename(image_path)

            try:
                shutil.move(
                    image_path,
                    os.path.join(get_config().PROCESSED_IMAGE_DIR, file_name)
                )
            except Exception as e:
                logger.error("Failed to move image '%s' to '%s'.",
                    file_name, get_config().PROCESSED_IMAGE_DIR, exc_info=True)
                raise e

        logger.info("Images moved to '%s' folder.", get_config().PROCESSED_IMAGE_DIR)
