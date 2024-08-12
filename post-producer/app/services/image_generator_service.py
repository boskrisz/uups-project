import os
import random
from typing import Tuple

import textwrap
from PIL import Image, ImageDraw, ImageFont

from app.config import get_config
from app.config.log_config import logger
from app.exceptions.image_generator_exceptions import TextDrawingException


class ImageGeneratorService:
    """
    Service class responsible for the logic of placing text quotes on images.

    Attributes:
        - image_size: The size of the generated image.
        - image_margin: The margin of the image.
        - quote_color: The color of the quote text.
        - quote_font_size: The font size of the quote text.
        - quote_offset: The offset of the quote text from the center.
    """
    def __init__(self, image_size: Tuple[int, int] = (2000, 2000),
            image_margin: int = 151,
            quote_color: Tuple[int, int, int] = (0, 0, 0),
            quote_font_size: int = 140,
            quote_offset: int = 100):
        # Set image properties
        self.image_size = image_size
        self.image_margin = image_margin
        self.image_background = None
        # Set quote properties
        self.quote_color = quote_color
        self.quote_font_size = quote_font_size
        self.quote_offset = quote_offset
        self.quote_font = None
        # Font and background options
        self.fonts = [
            get_config().QUOTE_FONT_BARRIO,
            get_config().QUOTE_FONT_MODAK,
            get_config().QUOTE_FONT_RUBIK,
        ]
        self.backgrounds = [
            get_config().BACKGROUND_YELLOW,
            get_config().BACKGROUND_PINK,
            get_config().BACKGROUND_PURPLE,
        ]


    def set_random_color_and_font_scheme(self):
        """
        Sets the color and font scheme for the image via random selection.
        Currently, there are 3 fonts and 3 backgrounds to choose from.
        """
        # Randomly select a font and background
        self.quote_font = random.choice(self.fonts)
        self.image_background = random.choice(self.backgrounds)

        # Load the font and background assets
        self.quote_font = ImageFont.truetype(
            font=self.quote_font,
            size=self.quote_font_size
        )
        self.image_background = Image.open(self.image_background)


    def create_image_with_quote(self, quote: str) -> Image.Image:
        """
        Creates an image with the given quote, using the pre-configured font and background.
        The quote is wrapped to fit the image width and centered on the image.

        Args:
            - quote: The quote to place on the image.
        """
        try:
            # Load image as Drawing object
            d = ImageDraw.Draw(self.image_background)

            # Wrap quote text to fit the image width
            wrapped_quote = textwrap.wrap(quote, width=20) # width in characters

            # Get center-center position for the wrapped quote text and serial num
            x_quote, y_quote = self.get_quote_position(wrapped_quote, self.quote_font)

            # Add quote to image
            d.text(
                xy=(x_quote, y_quote),
                text='\n'.join(wrapped_quote),
                font=self.quote_font,
                fill=self.quote_color,
                align="center",
                spacing=30
            )

            return self.image_background
        except Exception as e:
            logger.error("Failed to place quote on image.", exc_info=True)
            raise TextDrawingException() from e


    def get_quote_position(self, wrapped_quote: list[str],
        quote_font: ImageFont.FreeTypeFont) -> Tuple[int, int]:
        """
        Get the x and y position for the quote text.
        - The x position is calculated to center the text horizontally.
        - The y position is calculated to center the text vertically given the base offset.

        Args:
            - wrapped_quote: The quote text wrapped to fit the image width.
            - quote_font: The font to use for the quote
        """
        # Calculate the maximum width and total height of the wrapped quote
        max_width = 0
        total_height = 0
        for line in wrapped_quote:
            width = quote_font.getlength(line)
            max_width = max(max_width, width)
            total_height += quote_font.size

        # Get center position for the quote
        x_quote = (self.image_size[0] - max_width) // 2

        # Get y position for the quote
        y_quote = (self.image_size[1] - total_height) // 2 - self.quote_offset

        return x_quote, y_quote


    def get_meta(self) -> dict:
        """
        Returns the metadata of the image generator.
        """
        return {
            'quote_font': os.path.basename(self.quote_font.path),
            'image_background': os.path.basename(self.image_background.filename),
            'image_width': self.image_size[0],
            'image_height': self.image_size[1],
            'image_margin': self.image_margin,
            'quote_color': self.quote_color,
            'quote_font_size': self.quote_font_size,
            'quote_offset': self.quote_offset
        }
