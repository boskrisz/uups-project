import os
import logging

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from config import init_config
from clients.database_client import CosmosDbClient
from clients.storage_client import AzureStorageClient
from clients.social_media_client import InstagramClient
from services.asset_manager_service import AssetManagerService
from services.social_media_manager_service import SocialMediaManagerService


# Initialize the Azure Function App
app = func.FunctionApp()

# Python v2 model currently does not support the use of Microsoft Entra ID
# for authentication in function bindings.
# Therefore, the bindings initialization is done in the main function.
@app.schedule(schedule="0 0 17 * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    """
    Timer trigger function that runs every day at 17:00 and checks for unpublished approved images.
    In the case of any, it will pick one and publish it to the configured social media accounts.
    
    This is the entry point for the Azure Function App.
    """
    main()


def main():
    """
    Main process of the Azure Function App, separated from the entry point for testing purposes.
    """
    logging.info('Function execution started.')

    # Set the environment configuration
    config = init_config(os.environ['UUPS_ENV'])

    # Initialize authentication with managed identity
    default_credential = DefaultAzureCredential()

    # Initialize the asset manager for Azure Storage Account and Cosmos DB
    asset_manager_service = AssetManagerService(
        storage_client=AzureStorageClient(
            account_url=config.STORAGE_ACCOUNT_URL,
            container_name=config.STORAGE_CONTAINER_NAME,
            credential=default_credential
        ),
        database_client=CosmosDbClient(
            account_url=config.COSMOSDB_ACCOUNT_URL,
            database_name=config.COSMOSDB_DATABASE_NAME,
            container_name=config.COSMOSDB_CONTAINER_NAME,
            credential=default_credential
        )
    )

    # Check if there are any unpublished approved images
    image_meta = asset_manager_service.get_approved_image_meta()
    if not image_meta:
        logging.info("No unpublished images found.")
        return

    # Retrieve the image from the blob storage
    img_path = asset_manager_service.get_image_path(image_meta)

    # Initialize the Key Vault service that stores social media account credentials
    key_vault_client = SecretClient(config.KEYVAULT_URL, default_credential)

    # Initialize the social media manager service
    social_media_manager_service = SocialMediaManagerService(key_vault_client)
    social_media_manager_service.add_social_media_account(InstagramClient())

    # Upload post to all registered social media accounts
    social_media_manager_service.publish_posts(
        image_path=img_path,
        caption=image_meta['caption']
    )

    # Update the published status of the image in the database
    asset_manager_service.update_published_status(image_meta)

    logging.info('Function execution completed successfully.')
