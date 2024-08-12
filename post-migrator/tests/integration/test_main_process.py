import os
import csv

from PIL import Image

from app.__main__ import main
from app.config import get_config
from app.clients.database_client import CosmosDbClient
from app.clients.storage_client import AzureStorageClient
from app.models.image_meta import ImageMeta


def test_main_process(test_cosmosdb_client: CosmosDbClient,
    test_storage_account_client: AzureStorageClient,
    make_image_meta):
    """
    GIVEN a test Cosmos DB instance
        AND a test Azure Storage account
        AND some dummy approved images and their metadata
    WHEN the main process is called to migrate these assets to the cloud
    THEN the asset metadata should be inserted into the database
        AND they should receive a not published status
        AND the assets should be uploaded to the cloud storage account
        AND the approved images should be moved out of the local directory
    """
    # Initialize the dummy images metadata
    image_meta_1: ImageMeta = make_image_meta(id="test_id_1")
    image_meta_2: ImageMeta = make_image_meta(id="test_id_2")
    # Append them to the metadata csv file
    with open(get_config().IMAGE_META_FILE, 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(image_meta_1.to_list())
        writer.writerow(image_meta_2.to_list())

    # Create the dummy images
    image = Image.new('RGB', (10, 10))
    image_name_1 = image_meta_1.id + '.jpg'
    image_name_2 = image_meta_2.id + '.jpg'
    image_path_1 = os.path.join(get_config().APPROVED_IMAGE_DIR, image_name_1)
    image_path_2 = os.path.join(get_config().APPROVED_IMAGE_DIR, image_name_2)
    image.save(image_path_1)
    image.save(image_path_2)

    # Call the main process
    main()

    # Check that the metadata was inserted into the database
    query = "SELECT * FROM c WHERE c.id IN (@id0, @id1)"
    parameters = [
        {"name": "@id0", "value": image_meta_1.id},
        {"name": "@id1", "value": image_meta_2.id}
    ]
    results = list(test_cosmosdb_client.container_client.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))
    assert len(results) == 2
    assert { result['id'] for result in results } == { image_meta_1.id, image_meta_2.id }

    # Check that the metadata was marked as not published
    assert all(result['published'] is False for result in results)

    # Check that the assets were uploaded to the cloud storage account
    container_client = test_storage_account_client.container_client
    assert container_client.get_blob_client(image_name_1).exists()
    assert container_client.get_blob_client(image_name_2).exists()

    # Check that the approved images were moved to the processed folder
    assert len(os.listdir(get_config().APPROVED_IMAGE_DIR)) == 0
    assert os.path.exists(os.path.join(get_config().PROCESSED_IMAGE_DIR, image_name_1))
    assert os.path.exists(os.path.join(get_config().PROCESSED_IMAGE_DIR, image_name_2))
