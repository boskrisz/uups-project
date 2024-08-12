import os
import json
from csv import DictReader

from PIL import Image

from app.config import get_config
from app.models.image_meta import ImageMeta
from app.services.asset_manager_service import AssetManagerService


def test_save_image():
    """
    GIVEN a dummy image and an asset id
    WHEN the asset manager service is called to save the image
    THEN the image should be saved with the correct name
        AND to the correct directory
    """
    # Initialize dummy values
    generated_image = Image.new('RGB', (60, 30), color='red')
    asset_id = 'test_asset_id'

    # Save the image with the image directory patched
    AssetManagerService.save_image(generated_image, asset_id)

    # Check if the image is saved correctly
    assert os.path.exists(os.path.join(get_config().BASE_IMAGE_DIR, asset_id + '.jpg'))


def test_save_image_meta():
    """
    GIVEN some dummy asset metadata
    WHEN the asset manager service is called to save the asset metadata
    THEN the metadata should be saved correctly
    """
    # Initialize dummy values
    image_meta = ImageMeta(
        quote='test_quote',
        caption='test_caption',
        llm_model='test_llm_model',
        prompt_version='test_prompt_version',
        prompt_extras={
            'test_key': 'test_value'
        },
        img_meta={
            'test_key': 'test_value'
        }
    )

    # Save the metadata
    AssetManagerService.save_image_meta(image_meta)

    # Check if the metadata is saved correctly
    with open(get_config().IMAGE_META_FILE, 'r', encoding='utf-8') as f:
        dr = DictReader(f)
        inserted_row = list(dr)[0]

    assert inserted_row['quote'] == image_meta.quote
    assert inserted_row['caption'] == image_meta.caption
    assert inserted_row['llm_model'] == image_meta.llm_model
    assert inserted_row['prompt_version'] == image_meta.prompt_version
    assert json.loads(inserted_row['prompt_extras']) == image_meta.prompt_extras
    assert json.loads(inserted_row['img_meta']) == image_meta.img_meta
