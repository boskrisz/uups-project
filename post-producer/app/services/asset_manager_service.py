import os
import csv
import json

from PIL import Image

from app.config import get_config
from app.config.log_config import logger
from app.models.image_meta import ImageMeta


class AssetManagerService:
    """
    Service class responsible for managing the lifecycle of images and their metadata.
    """
    @staticmethod
    def save_image(generated_image: Image.Image,
        asset_id: str) -> None:
        """
        Saves the generated image under the configured directory.

        Args:
            - generated_image: The image to save.
            - asset_id: The name of the image when saved.
        """
        try:
            generated_image.save(os.path.join(get_config().BASE_IMAGE_DIR, asset_id + '.jpg'))
            logger.info("Image with name %s saved.", asset_id+'.jpg')
        except Exception as e:
            logger.error("Failed to save image for asset with id '%s'", asset_id, exc_info=True)
            raise e


    @staticmethod
    def save_image_meta(image_meta: ImageMeta) -> None:
        """
        Save the metadata of the generated image.

        Args:
            - image_meta: The metadata of the generated image
        """
        try:
            with open(get_config().IMAGE_META_FILE, mode='a', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow([
                    image_meta.id,
                    image_meta.quote,
                    image_meta.caption,
                    image_meta.llm_model,
                    image_meta.prompt_version,
                    json.dumps(image_meta.prompt_extras),
                    json.dumps(image_meta.img_meta)
                ])

            logger.info("Image metadata saved.")
        except Exception as e:
            logger.error("Failed to save asset metadata.", exc_info=True)
            raise e
