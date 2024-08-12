from typing import Tuple

from app.config.log_config import logger
from app.models.quote_generator_client import QuoteGeneratorClient
from app.exceptions.quote_generator_exceptions import (
    LlmOutputGenerationException,
    LlmOutputParsingException
)


class QuoteGeneratorService:
    """
    Service class that abstracts the logic for generating quotes and captions.
    """
    def __init__(self, client: QuoteGeneratorClient):
        self.client = client


    def get_quote_and_caption(self, prompt: str = None) -> Tuple[str, str]:
        """
        Generate a quote and caption using the provided LLM client.

        Args:
            prompt: The prompt to use for generating the quote and caption.
        """
        try:
            return self.client.generate_quote_and_caption(prompt)
        except LlmOutputGenerationException as e:
            logger.critical("%s failed to generate quote and caption.", e.llm_model, exc_info=True)
            raise e
        except LlmOutputParsingException as e:
            logger.critical("Failed to parse the output of %s.", e.llm_model, exc_info=True)
            raise e
