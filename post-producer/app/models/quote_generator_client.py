import json
from typing import Tuple
from abc import ABC, abstractmethod

from openai import OpenAI

from app.config import get_config
from app.exceptions.quote_generator_exceptions import (
    LlmOutputGenerationException,
    LlmOutputParsingException
)


class QuoteGeneratorClient(ABC):
    """
    Abstract base class for a quote generator client.
    """
    @abstractmethod
    def generate_output(self, prompt: str) -> dict:
        """
        Generate an output for the given prompt.

        Args:
            - prompt: The prompt to generate the output.
        """
        pass


    @abstractmethod
    def generate_quote_and_caption(self, prompt: str) -> Tuple[str, str]:
        """
        Generate a quote with a relevant caption based on the given prompt.

        Args:
            - prompt: The prompt to generate the quote and caption.
        """
        pass


class OpenAiClient(QuoteGeneratorClient):
    """
    Client class responsible for interacting with OpenAI's GPT-4 API.

    Attributes:
        - client: The OpenAI client instance.
        - model: The LLM model to use for generating the output.
    """
    def __init__(self, api_key: str = None,
        model: str = None):
        self.model = model
        self.client = OpenAI(api_key=api_key)


    def generate_quote_and_caption(self, prompt: str) -> Tuple[str, str]:
        """
        Generate a quote with a relevant caption using GPT-4, based on the given prompt.

        The given prompt must enforce the GPT agent to return a JSON object 
        with the keys 'quote' and 'caption'.

        Args:
            - prompt: The prompt to generate the quote and caption.
        """
        # Generate the quote and caption using the GPT model
        output = self.generate_output(prompt)

        # Parse the response from the GPT model
        quote, caption = self.parse_output(output)

        return quote, caption


    def generate_output(self, prompt: str) -> dict:
        """
        Generate a an output for the given prompt using the GPT model.

        Args:
            - prompt: The prompt to generate the output.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                response_format={ "type": "json_object" },
                messages=[{
                        "role": "user",
                        "content": prompt
                    }],
            )

            # Retrieve the generated answer from the completion
            return completion.choices[0].message.content
        except Exception as e:
            raise LlmOutputGenerationException(llm_model=self.model) from e


    def parse_output(self, output: dict) -> Tuple[str, str]:
        """
        Parse the output from the GPT model to extract the quote and caption.

        The given output must be a dumped JSON object with the keys 'quote' and 'caption'.

        Args:
            - output: The generated JSON output from the GPT model.
        """
        try:
            response = json.loads(output)
            quote = response['quote']
            caption = response['caption']
        except Exception as e:
            raise LlmOutputParsingException(llm_model=self.model) from e

        return quote, caption
