from PIL import ImageFont

from app.config import get_config
from app.exceptions.image_generator_exceptions import TextDrawingException
from app.services.image_generator_service import ImageGeneratorService


def test_get_quote_position_returns_center_coordinates():
    """
    GIVEN a list of wrapped quotes
        AND a base image
        AND this quote has a font size and offset when placed on the image
    WHEN the quote's position on the base image is calculated
    THEN the center coordinates of the quote should be returned
    """
    # Initialize objects
    wrapped_quote = ['']
    font = ImageFont.truetype(font=get_config().QUOTE_FONT_BARRIO, size=12)
    image_generator_service = ImageGeneratorService(
        image_size=(100, 100),
        image_margin=0,
        quote_offset=4
    )

    # Get the center coordinates
    x_quote, y_quote = image_generator_service.get_quote_position(wrapped_quote, font)

    # Check if the center coordinates are correct
    assert x_quote == 50
    assert y_quote == 40 # 50 - 6 (half of font size) - 4 (offset)


def test_create_image_with_quote_does_not_raise_exception():
    """
    GIVEN a quote and a base image
    WHEN the quote is placed on the base image
    THEN the method should not raise an exception
    """
    # Initialize objects
    quote = 'test_quote'
    image_generator_service = ImageGeneratorService()
    image_generator_service.set_random_color_and_font_scheme()

    # Create the image with the quote
    try:
        image_generator_service.create_image_with_quote(quote)
    except TextDrawingException as e:
        assert False, e
