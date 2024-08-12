from app.config import init_config, get_config
from app.config.log_config import logger
from app.clients.database_client import CosmosDbClient
from app.clients.storage_client import AzureStorageClient
from app.services.asset_manager_service import AssetManagerService


def main():
    # Initialize the AssetManagerService for Azure Blob Storage and Azure Cosmos DB
    asset_manager_service = AssetManagerService(
        storage_client=AzureStorageClient(
            account_url=get_config().STORAGE_ACCOUNT_URL,
            container_name=get_config().STORAGE_CONTAINER_NAME,
            sas_token=get_config().STORAGE_CONTAINER_SAS
        ),
        database_client=CosmosDbClient(
            account_url=get_config().COSMOSDB_ACCOUNT_URL,
            account_key=get_config().COSMOSDB_ACCOUNT_KEY,
            database_name=get_config().COSMOSDB_DATABASE_NAME,
            container_name=get_config().COSMOSDB_CONTAINER_NAME
        )
    )

    # Get the approved images and their metadata
    img_paths, img_metas = asset_manager_service.get_approved_assets()

    if not img_paths:
        logger.info("No approved images to upload.")
        return

    # Upload the approved images to the cloud storage and their metas to the database
    asset_manager_service.upload_images(img_paths)
    asset_manager_service.upload_image_metas(img_metas)

    # Move locally the approved images to the processed folder
    asset_manager_service.move_images_to_processed(img_paths)


if __name__ == "__main__":
    # Initialize the project configuration
    init_config(env='prod')

    main()
