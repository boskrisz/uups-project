class DatabaseInsertException(Exception):
    """
    Exception raised when a record insertion into the cloud database fails.
    """
    def __init__(self, cloud_database_name: str,
        message="Failed to insert record into the Cloud Database."
        ):
        super().__init__(message)
        self.cloud_database_name = cloud_database_name
