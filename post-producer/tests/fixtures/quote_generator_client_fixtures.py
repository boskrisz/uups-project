import json
from typing import Generator

from unittest.mock import patch, MagicMock
import pytest

from app.models.quote_generator_client import OpenAiClient


def init_client_side_effect(self, 
    api_key: str = "mock_api_key",
    model: str = "mock_model"):
    """
    Mimick the OpenAI client instance initialization with a mocked client.
    """
    self.model = model
    self.client = MagicMock()


@pytest.fixture
def mock_openai_client() -> Generator[OpenAiClient, None, None]:
    """
    Mock the OpenAI client instance.
    """
    with patch.object(OpenAiClient, '__init__',
            new=lambda self,
            model="mock_model",
            api_key="mock_api_key",
            : init_client_side_effect(self, api_key, model)
        ), \
        patch.object(OpenAiClient, 'generate_output',
            MagicMock(return_value=json.dumps(
                {
                    "quote": "mock_quote", 
                    "caption": "mock_caption"
                }
            ))
        ):

        mock_instance = OpenAiClient()
        yield mock_instance
