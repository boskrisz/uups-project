import os
from csv import DictReader

from app.__main__ import main
from app.config import get_config


def test_main_process(mock_openai_client):
    """
    GIVEN the number of images to generate
        AND a mocked OpenAI client instance that returns a dummy quote
    WHEN the main process is called to generate images
    THEN the specified number of images should be generated
        AND the images' metadata should be saved
    """
    # Initialize values
    image_num = 2

    # Call the main process
    main(image_num=image_num)

    # Check if the images were generated
    images = os.listdir(get_config().BASE_IMAGE_DIR)
    assert len(images) == image_num

    # Check if the metadata was saved correctly
    with open(get_config().IMAGE_META_FILE, 'r', encoding='utf-8') as f:
        dr = DictReader(f)
        inserted_rows = list(dr)

    assert len(inserted_rows) == image_num
    assert set(image.split('.')[0] for image in images) == set(row['id'] for row in inserted_rows)
    assert all([row['quote'] == 'mock_quote' for row in inserted_rows])
    assert all([row['caption'] == 'mock_caption' for row in inserted_rows])
    assert all([row['prompt_extras'] is not None for row in inserted_rows])
