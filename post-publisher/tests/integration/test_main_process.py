from azure.keyvault.secrets import SecretClient

from function_app import main
from config import get_config
from clients.database_client import CosmosDbClient
from clients.social_media_client import InstagramClient


def test_main_process(mock_instagram_client: InstagramClient,
    mock_key_vault_client: SecretClient,
    test_cosmosdb_client: CosmosDbClient,
    dummy_img_in_blob_storage: str,
    dummy_img_meta_in_db: dict,
    ):
    """
    GIVEN a dummy image uploaded to a Blob Storage
        AND its relevant metadata document in a Cosmos DB container
        AND a mocked Instagram client instance
        AND a mocked Key Vault that would store the client's access token
    WHEN the timer trigger function is executed
    THEN Instagram client's publish method should be called with the correct parameters
        AND the metadata document should be updated with the published status
    """
    # Execute the main process
    main()

    # Check if the Instagram client's publish method was called with the correct parameters
    mock_instagram_client.publish_post.assert_called_once()
    _, kwargs = mock_instagram_client.publish_post.call_args
    assert kwargs['image_path'].split('?')[0] \
        == get_config().STORAGE_ACCOUNT_URL + "generated-assets/" + dummy_img_in_blob_storage
    assert kwargs['caption'] == dummy_img_meta_in_db['caption']
    assert kwargs['account_id'] \
        == mock_key_vault_client.get_secret("instagram-account-id").value
    assert kwargs['access_token'] \
        == mock_key_vault_client.get_secret("instagram-access-token").value

    # Check if the metadata document was updated
    updated_meta = test_cosmosdb_client.container_client.read_item(
        item=dummy_img_meta_in_db['id'],
        partition_key=dummy_img_meta_in_db['id']
    )
    assert updated_meta['published'] is True
