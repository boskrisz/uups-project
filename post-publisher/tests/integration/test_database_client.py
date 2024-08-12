from clients.database_client import CosmosDbClient


def test_find_one_by_published(test_cosmosdb_client: CosmosDbClient):
    """
    GIVEN a test Cosmos DB instance
        AND some dummy records with published status properties
    WHEN the method to find records based on their published status is called
    THEN it should return a correct record
    """
    # Insert some records with published status properties
    test_cosmosdb_client.container_client.upsert_item({
        "id": "123",
        "published": False
    })
    test_cosmosdb_client.container_client.upsert_item({
        "id": "456",
        "published": True
    })

    # Retrieve a single document from the Cosmos DB container based on the published status
    result = test_cosmosdb_client.find_one_by_published(False)

    # Check the result
    assert result["id"] == "123"
    assert result["published"] is False


def test_update_published_status(test_cosmosdb_client: CosmosDbClient):
    """
    GIVEN a test Cosmos DB instance
        AND a dummy record with published status set to False
    WHEN the method to update the published status of the record is called
    THEN the record should be updated with the new published status
    """
    # Insert the dummy records
    test_cosmosdb_client.container_client.upsert_item({
        "id": "123",
        "published": False
    })

    # Update the published status of the record
    test_cosmosdb_client.update_published_status("123", True)

    # Retrieve the updated record
    result = test_cosmosdb_client.container_client.read_item("123", "123")

    # Check the result
    assert result["id"] == "123"
    assert result["published"] is True
