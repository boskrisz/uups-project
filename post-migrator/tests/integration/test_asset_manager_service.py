import os
import csv

from PIL import Image

from app.config import get_config
from app.services.asset_manager_service import AssetManagerService


def test_get_approved_image_paths_finds_all_approved_images():
    """
    GIVEN some dummy images in the approved images directory
    WHEN the list of images in the directory is retrieved
    THEN the list should contain all the dummy images' names
    """
    # Create some dummy images in the approved images directory
    dummy_images = ['image1.jpg', 'image2.jpg', 'image3.jpg']
    dummy_image_paths = set()
    for img in dummy_images:
        # Create a blank image
        image = Image.new('RGB', (10, 10))

        # Save the image as JPG
        image_path = os.path.join(get_config().APPROVED_IMAGE_DIR, img)
        image.save(image_path)
        dummy_image_paths.add(image_path)

    # Get the paths of the approved images
    approved_image_paths = AssetManagerService.get_approved_image_paths()

    # Check that the list of approved images contains all the dummy images
    assert set(approved_image_paths) == dummy_image_paths


def test_get_approved_image_metas_finds_only_approved_image_metas():
    """
    GIVEN a dummy image metadata file with some approved and non-approved images
    WHEN the metadata of the approved images is retrieved
    THEN the metadata should only contain the approved images' metadata
    """
    # Initialize some dummy images
    approved_image_ids = ['image1', 'image2', 'image3']
    non_approved_image_ids = ['image4', 'image5']
    image_ids = approved_image_ids + non_approved_image_ids
    approved_image_paths = [os.path.join(get_config().APPROVED_IMAGE_DIR, f'{img}.jpg')
        for img in approved_image_ids]

    # Create a dummy image metadata file
    with open(get_config().IMAGE_META_FILE, mode='a', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        for img_id in image_ids:
            # Written in ImageMeta format
            writer.writerow([
                img_id,
                'quote',
                'caption',
                'llm_model',
                'prompt_version',
                '{}',
                '{}'
            ])

    # Get the metadata of the approved images
    approved_metas = AssetManagerService.get_approved_image_metas(approved_image_paths)

    # Check that the metadata only contains the approved images' metadata
    assert { meta.id for meta in approved_metas } == set(approved_image_ids)


def test_processed_images_are_moved_to_processed_folder():
    """
    GIVEN some dummy images in the approved images directory
    WHEN the images are processed
    THEN the images should be moved to the processed folder
    """
    # Create some dummy images in the approved images directory
    dummy_images = ['image1.jpg', 'image2.jpg', 'image3.jpg']
    dummy_image_paths = []
    for img in dummy_images:
        # Create a blank image
        image = Image.new('RGB', (10, 10))

        # Save the image as JPG
        image_path = os.path.join(get_config().APPROVED_IMAGE_DIR, img)
        image.save(image_path)
        dummy_image_paths.append(image_path)

    # Move the images to the processed folder
    AssetManagerService.move_images_to_processed(dummy_image_paths)

    # Check that the images were moved to the processed folder
    for old_img_path in dummy_image_paths:
        new_img_path = os.path.join(
            get_config().PROCESSED_IMAGE_DIR, 
            os.path.basename(old_img_path)
        )

        assert not os.path.exists(old_img_path)
        assert os.path.exists(new_img_path)
