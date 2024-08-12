class TextDrawingException(Exception):
    """
    Exception raised when an error occurs during placing a text on an image.
    """
    def __init__(self,
        message: str = "Failed to draw text on the image."
        ):
        super().__init__(message)
