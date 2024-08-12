import pytest

from app.models.image_meta import ImageMeta


@pytest.fixture
def make_image_meta():
    """
    Return a function that creates an ImageMeta instance with the specified attributes.
    """
    def get_image_meta_config(id: str = "e76382ed-23fd-40c2-b5c5-7b481b73b08c",
        quote: str = "test_quote",
        caption: str = "test_caption",
        llm_model: str = "test_llm_model",
        prompt_version: str = "1.0.0",
        prompt_extras: dict = None,
        img_meta: dict = None) -> ImageMeta:

        # Initialize mutable default arguments
        prompt_extras = prompt_extras or {}
        img_meta = img_meta or {}

        image_meta = ImageMeta(
            id=id,
            quote=quote,
            caption=caption,
            llm_model=llm_model,
            prompt_version=prompt_version,
            prompt_extras=prompt_extras,
            img_meta=img_meta
        )

        return image_meta
    return get_image_meta_config
