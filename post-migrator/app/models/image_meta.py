import json
from dataclasses import dataclass, fields


@dataclass
class ImageMeta:
    """
    This class holds meta information of the generated image.

    Attributes:
        - id: The unique identifier of the image.
        - quote: The quote used to generate the image.
        - caption: The caption for the image.
        - llm_model: The language model used to generate the image.
        - prompt_version: The version of the prompt used to generate the image.
        - prompt_extras: Extra information about the prompt used to generate the image.
        - img_meta: Meta information about the generated image.
    """
    id: str
    quote: str
    caption: str
    llm_model: str
    prompt_version: str
    prompt_extras: dict
    img_meta: dict


    @staticmethod
    def get_field_names() -> list[str]:
        """
        Get the field names of the ImageMeta class.
        """
        return [field.name for field in fields(ImageMeta)]


    def to_json(self) -> dict:
        """
        Convert the ImageMeta object to a dictionary.
        """
        return {
            "id": self.id,
            "quote": self.quote,
            "caption": self.caption,
            "llm_model": self.llm_model,
            "prompt_version": self.prompt_version,
            "prompt_extras": json.dumps(self.prompt_extras),
            "img_meta": json.dumps(self.img_meta)
        }


    def to_list(self) -> list:
        """
        Convert the ImageMeta object to a list.
        """
        return [
            self.id,
            self.quote,
            self.caption,
            self.llm_model,
            self.prompt_version,
            json.dumps(self.prompt_extras),
            json.dumps(self.img_meta)
        ]
