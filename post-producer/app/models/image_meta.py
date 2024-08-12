import uuid
from dataclasses import dataclass, field, fields


@dataclass
class ImageMeta:
    """
    This class holds meta information of the generated image.

    Currently, the order of the fields is important as this class initializes the .csv file,
    where their data will be stored.

    Attributes:
        - id: The unique identifier of the image.
        - quote: The quote text on the image.
        - caption: The caption for the image.
        - llm_model: The language model used to generate the quote.
        - prompt_version: The version of the prompt used.
        - prompt_extras: Additional information about the prompt.
        - img_meta: Metadata about the image file.
    """
    # Use default factory to avoid issues with mutable default arguments
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    quote: str = None
    caption: str = None
    llm_model: str = None
    prompt_version: str = None
    prompt_extras: dict = None
    img_meta: dict = None

    @staticmethod
    def get_field_names() -> list[str]:
        """
        Get the field names of the ImageMeta class.
        """
        return [field.name for field in fields(ImageMeta)]


    def update(self, **kwargs):
        """
        Update the given attributes of the ImageMeta instance.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Attribute '{key}' not found in ImageMeta.")
