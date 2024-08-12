from abc import ABC, abstractmethod
from typing import Any, Dict, Union

from azure.cosmos.cosmos_client import CosmosClient
from azure.identity import DefaultAzureCredential

from exceptions.database_client_exceptions import (
    DatabaseSelectQueryException,
    DatabaseUpdateQueryException
)


class DatabaseClient(ABC):
    """
    Abstract class for a database client.
    """
    @abstractmethod
    def find_one_by_published(self, published: bool) -> dict:
        """
        Retrieve a single document from the database based on the published status.

        Args:
            - published: Whether the post has already been published to social media or not.
        """
        pass

    @abstractmethod
    def update_published_status(self, document_id: str,
        published: bool) -> None:
        """
        Update the published status of a document in the database.

        Args:
            - document_id: The ID of the document to be updated.
            - published: Whether the post has already been published to social media or not.
        """
        pass


class CosmosDbClient(DatabaseClient):
    """
    Client class for interacting with Azure Cosmos DB.

    Attributes:
        - account_url: The URL of the Azure Cosmos DB account.
        - database_name: The name of the database within the Azure Cosmos DB account.
        - container_name: The name of the container within the Azure Cosmos DB database.
        - cosmos_client: The Azure Cosmos DB client instance.
        - database_client: The Azure Cosmos DB database client instance.
        - container_client: The Azure Cosmos DB container client instance.
    """
    def __init__(self, account_url: str,
        database_name: str,
        container_name: str,
        credential: DefaultAzureCredential) -> None:
        self.account_url = account_url
        self.database_name = database_name
        self.container_name = container_name
        # Create the Azure Cosmos DB clients
        self._init_database_client(credential)
        self.init_container_client(container_name)


    def _init_database_client(self,
        credential: Union[DefaultAzureCredential, Dict[str, Any]]) -> None:
        """
        Initialize a database client that can be used to interact with the Azure Cosmos DB.

        Args:
            - key: The account key for the Azure Cosmos DB.
            It can be either an Azure managed identity or a master key.
        """
        self.cosmos_client = CosmosClient(
            url=self.account_url,
            credential=credential
        )
        self.database_client = self.cosmos_client.get_database_client(self.database_name)


    def init_container_client(self, container_name: str) -> None:
        """
        Initialize a container client that can be used to interact 
        with a given container in the Azure Cosmos DB.

        Args:
            - container_name: The ID or name of the container in the database.
        """
        # Initialize the container client
        self.container_client = self.database_client.get_container_client(container_name)


    def find_one_by_published(self, published: bool) -> Union[dict, None]:
        """
        Retrieve a single document from the Cosmos DB container based on the published status.

        Args:
            - published: Whether the post has already been published to social media or not.
        """
        query = "SELECT TOP 1 * FROM c WHERE c.published = @published"
        parameters = [{"name": "@published", "value": published}]

        try:
            results = list(self.container_client.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
        except Exception as e:
            raise DatabaseSelectQueryException(cloud_database_name="Azure Cosmos DB") from e

        return results[0] if len(results) > 0 else None


    def update_published_status(self, document_id: str,
        published: bool) -> None:
        """
        Update the published status of a document in the Cosmos DB container.

        Args:
            - document_id: The ID of the document to update.
            - published: Whether the post has already been published to social media or not.
        """
        operations = [
            { 'op': 'set', 'path': '/published', 'value': published }
        ]

        try:
            self.container_client.patch_item(
                item=document_id,
                partition_key=document_id,
                patch_operations=operations
            )
        except Exception as e:
            raise DatabaseUpdateQueryException(cloud_database_name="Azure Cosmos DB") from e


    def delete_all_items_from_container(self) -> None:
        """
        Delete all items from the preconfigured database container.
        """
        assert "test" in self.account_url, \
            "This method should only be used in testing environments."

        # Query all items in the container
        items = list(self.container_client.query_items(
            query="SELECT * FROM c",
            enable_cross_partition_query=True
        ))

        # Delete all items in the container
        for item in items:
            self.container_client.delete_item(item=item['id'], partition_key=item['id'])
