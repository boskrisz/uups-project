import datetime
import logging
from abc import ABC, abstractmethod

from azure.identity import DefaultAzureCredential
from azure.storage.blob import (
    BlobServiceClient,
    BlobSasPermissions,
    UserDelegationKey,
    generate_blob_sas
)


class StorageClient(ABC):
    """
    Abstract class for a storage client.
    """
    @abstractmethod
    def get_access_token(self, file_name: str) -> None:
        """
        Get an access token for the given file.

        Args:
            - file_name: The name of the file to get the access token for.
        """
        pass


class AzureStorageClient(StorageClient):
    """
    A storage client for Azure Blob Storage.

    Attributes:
        - account_url: The URL of the Azure Storage Account.
        - container_name: The name of the container within the Azure Storage Account.
        - blob_service_client: The Azure Blob Storage client instance.
        - container_client: The Azure Blob Storage container client instance.
    """
    def __init__(self, account_url: str,
        container_name: str,
        credential: DefaultAzureCredential) -> None:
        self.account_url = account_url
        self.container_name = container_name
        # Create a client that will access the blobs in the Storage Account's container
        self._init_blob_service_client(credential)


    def _init_blob_service_client(self, credential: DefaultAzureCredential) -> None:
        """
        Initialize the Azure Blob Storage container client.

        Args:
            - credential: The Azure credential to authenticate the client.
        """
        self.blob_service_client = BlobServiceClient(
            account_url=self.account_url,
            container_name=self.container_name,
            credential=credential
        )
        self.container_client = self.blob_service_client.get_container_client(self.container_name)


    def _request_user_delegation_key(self) -> UserDelegationKey:
        """
        Request a user delegation key for signing SAS tokens 
        that enables permissioned access to blobs in the authenticated Storage Account.
        """
        # Get a short-lived user delegation key that's valid for 5 minutes
        delegation_key_start_time = datetime.datetime.now(datetime.timezone.utc)
        delegation_key_expiry_time = delegation_key_start_time + datetime.timedelta(minutes=5)

        try:
            user_delegation_key = self.blob_service_client.get_user_delegation_key(
                key_start_time=delegation_key_start_time,
                key_expiry_time=delegation_key_expiry_time
            )
        except Exception as e:
            logging.error("Failed to get user delegation key.", exc_info=True)
            raise e

        return user_delegation_key


    def get_access_token(self, file_name: str) -> str:
        """
        Get a short-lived read-only access token for the given file.

        The SAS token is valid for 5 minutes, which is plenty of time for the 
        Azure Function's execution.

        Args:
            - file_name: The name of the file to get the access token for.
        """
        # Initialize a BlobClient for the given blob
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name,
            blob=file_name
        )

        # Create a short-lived read-only SAS token with a user delegation key
        user_delegation_key = self._request_user_delegation_key()
        start_time = datetime.datetime.now(datetime.timezone.utc)
        expiry_time = start_time + datetime.timedelta(minutes=5)

        try:
            sas_token = generate_blob_sas(
                account_name=blob_client.account_name,
                container_name=blob_client.container_name,
                blob_name=blob_client.blob_name,
                user_delegation_key=user_delegation_key,
                permission=BlobSasPermissions(read=True),
                expiry=expiry_time,
                start=start_time
            )
        except Exception as e:
            logging.error("Failed to generate SAS token.", exc_info=True)
            raise e

        return sas_token


    def delete_all_blobs_in_container(self) -> None:
        """
        Delete all blobs in the configured Azure Blob Storage container.
        """
        assert "test" in self.account_url, "Test environment must be used for this method"

        for blob in self.container_client.list_blobs():
            self.container_client.delete_blob(blob.name)
