from abc import ABC, abstractmethod

from azure.cosmos.cosmos_client import (
    CosmosClient,
    CosmosResourceNotFoundError
)

from app.config.log_config import logger
from app.exceptions.database_client_exceptions import DatabaseInsertException


class DatabaseClient(ABC):
    """
    Abstract class for a cloud database client.
    """
    @abstractmethod
    def insert_record(self, record: dict) -> None:
        """
        Insert a record into the cloud database.
        """
        pass


class CosmosDbClient(DatabaseClient):
    """
    Client class for interacting with the Azure Cosmos DB.

    Attributes:
        - account_url: The URL of the Azure Cosmos DB.
        - account_key: The account key for the Azure Cosmos DB.
        - database_name: The ID or name of the database in the Azure Cosmos DB.
        - container_name: The ID or name of the container in the Azure Cosmos.
    """
    def __init__(self, account_url: str,
        account_key: str,
        database_name: str,
        container_name: str) -> None:
        self.account_url = account_url
        self.database_name = database_name
        self.container_name = container_name
        # Create the Azure Cosmos DB clients
        self._init_database_client(account_key)
        self.init_container_client(self.container_name)


    def _init_database_client(self, key: str) -> None:
        """
        Initialize a database client that can be used to interact with the Azure Cosmos DB.

        Args:
            - key: The account key for the Azure Cosmos DB
        """
        self.cosmos_client = CosmosClient(
            url=self.account_url,
            credential={"masterKey": key}
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


    def container_exists(self, container_name: str) -> bool:
        """
        Check if a container exists in the Azure Cosmos DB.

        Args:
            - container_name: The ID or name of the container in the database.
        """
        try:
            container = self.database_client.get_container_client(container_name)
            # Attempt to read the container properties
            container.read()
            return True
        except CosmosResourceNotFoundError:
            return False


    def insert_record(self, record: dict) -> None:
        """
        Insert a record into the database's container.

        Args:
            - record: The record to be inserted into the database.
        """
        try:
            self.container_client.upsert_item(body=record)
        except Exception as e:
            logger.error("Failed to insert record into the Azure Cosmos DB.", exc_info=True)
            raise DatabaseInsertException(cloud_database_name="Azure Cosmos DB") from e


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
