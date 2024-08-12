class DatabaseSelectQueryException(Exception):
    """
    Exception raised when a select query fails to select a record from the cloud database.
    """
    def __init__(self, cloud_database_name: str,
        message="Failed to select a record from the cloud database."
        ):
        super().__init__(message)
        self.cloud_database_name = cloud_database_name


class DatabaseUpdateQueryException(Exception):
    """
    Exception raised when an update query fails to update a record in the cloud database.
    """
    def __init__(self, cloud_database_name: str,
        message="Failed to update a record in the cloud database."
        ):
        super().__init__(message)
        self.cloud_database_name = cloud_database_name
