from app.clients.database_client import CosmosDbClient
from app.models.image_meta import ImageMeta


def test_insert_record(test_cosmosdb_client: CosmosDbClient,
    make_image_meta):
    """
    GIVEN a test Cosmos DB instance
    WHEN its insert record method is called with a dummy record
    THEN it should insert the record into the database.
    """
    # Initialize a dummy record
    image_meta: ImageMeta = make_image_meta(id="test_id")

    # Insert the record into the database
    test_cosmosdb_client.insert_record(image_meta.to_json())

    # Check if the record was inserted
    query = "SELECT * FROM c WHERE c.id = @id"
    parameters = [{"name": "@id", "value": image_meta.id}]
    results = list(test_cosmosdb_client.container_client.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    assert len(results) == 1
    assert results[0]['id'] == image_meta.id
