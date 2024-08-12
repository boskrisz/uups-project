from abc import ABC, abstractmethod

from azure.storage.blob import ContainerClient, ContentSettings

from app.config.log_config import logger
from app.exceptions.storage_client_exceptions import FileUploadException


class StorageClient(ABC):
    """
    Abstract class for a cloud storage client.
    """
    @abstractmethod
    def upload_file(self, file_path: str,
        file_name: str) -> None:
        """
        Upload a file to the cloud storage.

        Args:
            - file_path: The path to the file to be uploaded.
            - file_name: The name of the file in the cloud storage.
        """
        pass


class AzureStorageClient(StorageClient):
    """
    Client class for interacting with an Azure Account Storage.

    Attributes:
        - account_url: The URL of the Azure Blob Storage account.
        - container_name: The name of the container in the Azure Blob Storage.
        - sas_token: The Shared Access Signature (SAS) token for the Azure Blob Storage.
    """
    def __init__(self, account_url: str,
        container_name: str,
        sas_token: str) -> None:
        self.account_url = account_url
        self.container_name = container_name
        # Create an Azure container client
        self._init_container_client(sas_token)


    def _init_container_client(self, credential: str) -> None:
        """
        Initialize the Azure Blob Storage container client.

        Args:
            - credential: The Azure credential to authenticate the client.
        """
        self.container_client = ContainerClient(
            account_url=self.account_url,
            container_name=self.container_name,
            credential=credential
        )


    def upload_file(self, file_path: str,
        file_name: str) -> None:
        """
        Upload a file to the Azure Blob Storage. 

        Args:
            - file_path: The path to the file to be uploaded.
            - file_name: The name of the file in the blob storage.
        """
        try:
            with open(file=file_path, mode="rb") as data:
                self.container_client.upload_blob(
                    name=file_name,
                    data=data,
                    content_settings=ContentSettings(
                        content_type="image/jpg"
                    )
            )
        except Exception as e:
            logger.error("Failed to upload file to the Azure Blob Storage.", exc_info=True)
            raise FileUploadException(cloud_storage_name="Azure Blob Storage") from e


    def delete_all_blobs_in_container(self) -> None:
        """
        Delete all blobs in the Azure Blob Storage container.
        """
        assert "test" in self.account_url, "Test environment must be used for this method"

        blobs = self.container_client.list_blobs()
        for blob in blobs:
            self.container_client.delete_blob(blob.name)
