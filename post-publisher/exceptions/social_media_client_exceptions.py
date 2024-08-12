class SocialMediaException(Exception):
    """
    Base exception class for social media client errors.
    """
    pass


class InstagramMediaUploadException(SocialMediaException):
    """
    Exception raised when an image fails to upload to Instagram's media container.

    Read more about the errors here:
    https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/error-codes
    """
    def __init__(self, error_code: int,
        error_message: str,
        message: str = "Failed to upload image to Instagram's media container."):
        super().__init__(message)
        self.error_code = error_code
        self.error_message = error_message


class InstagramMediaPublishException(SocialMediaException):
    """
    Exception raised when a post fails to publish to Instagram.

    Read more about the errors here:
    https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/error-codes
    """
    def __init__(self, error_code: int,
        error_message: str,
        message: str = "Failed to publish post to Instagram."):
        super().__init__(message)
        self.error_code = error_code
        self.error_message = error_message
