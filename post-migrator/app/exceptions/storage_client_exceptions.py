class FileUploadException(Exception):
    """
    Exception raised when a file upload to the cloud storage fails.
    """
    def __init__(self, cloud_storage_name: str,
        message="Failed to upload file to the Cloud Storage."
        ):
        super().__init__(message)
        self.cloud_storage = cloud_storage_name
